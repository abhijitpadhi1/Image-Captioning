import torch

from ..model.encoder import EncoderCNN
from ..model.decoder import DecoderWithAttention
from ..utils.model_utils import get_model_path


def load_model(device):
    model_path = get_model_path()
    checkpoint = torch.load(model_path, map_location=device)

    cfg = checkpoint["config"]

    encoder = EncoderCNN(pretrained=False).to(device)
    decoder = DecoderWithAttention(
        feature_dim=cfg["feature_dim"],
        embed_size=cfg["embed_size"],
        hidden_size=cfg["hidden_size"],
        vocab_size=cfg["vocab_size"]
    ).to(device)

    encoder.load_state_dict(checkpoint["encoder"], strict=True)
    decoder.load_state_dict(checkpoint["decoder"], strict=True)

    encoder.eval()
    decoder.eval()

    return encoder, decoder


def generate_caption_greedy(encoder, decoder, image, vocab, device, max_len=20):
    encoder.eval()
    decoder.eval()

    with torch.no_grad():
        image = image.to(device).unsqueeze(0)  # (1, 3, 224, 224)

        features = encoder(image)  # (1, 49, 2048)

        h = torch.zeros(1, decoder.lstm.hidden_size).to(device)
        c = torch.zeros(1, decoder.lstm.hidden_size).to(device)

        inputs = torch.tensor([vocab.stoi["<start>"]]).to(device)

        generated_caption = []

        for _ in range(max_len):
            embedding = decoder.embedding(inputs).squeeze(1)  # (1, E)

            # Attention step
            context, alpha = decoder.attention(features, h)

            lstm_input = torch.cat((embedding, context), dim=1)

            h, c = decoder.lstm(lstm_input, (h, c))

            output = decoder.fc(h)  # (1, vocab_size)

            predicted = output.argmax(1)

            word = vocab.itos[predicted.item()]

            if word == "<end>":
                break

            generated_caption.append(word)

            inputs = predicted

    return " ".join(generated_caption)


def generate_caption_beam(encoder, decoder, image, vocab, device, beam_width=3, max_len=20):
    encoder.eval()
    decoder.eval()

    with torch.no_grad():
        image = image.to(device).unsqueeze(0)
        features = encoder(image)  # (1, 49, 2048)

        sequences = [
            {
                "seq": [vocab.stoi["<start>"]],
                "score": 0.0,
                "h": torch.zeros(1, decoder.lstm.hidden_size).to(device),
                "c": torch.zeros(1, decoder.lstm.hidden_size).to(device),
            }
        ]

        for _ in range(max_len):
            all_candidates = []

            for seq_data in sequences:
                seq = seq_data["seq"]
                score = seq_data["score"]
                h = seq_data["h"]
                c = seq_data["c"]

                last_token = seq[-1]

                if last_token == vocab.stoi["<end>"]:
                    all_candidates.append(seq_data)
                    continue

                input_token = torch.tensor([last_token]).to(device)
                embedding = decoder.embedding(input_token)

                context, alpha = decoder.attention(features, h)

                lstm_input = torch.cat((embedding.squeeze(1), context), dim=1)

                h_new, c_new = decoder.lstm(lstm_input, (h, c))

                logits = decoder.fc(h_new)
                log_probs = torch.log_softmax(logits, dim=1)

                topk_probs, topk_indices = log_probs.topk(beam_width)

                for i in range(beam_width):
                    word = topk_indices[0][i].item()
                    new_seq = seq + [word]
                    new_score = score + topk_probs[0][i].item()

                    all_candidates.append({
                        "seq": new_seq,
                        "score": new_score,
                        "h": h_new,
                        "c": c_new,
                    })

            sequences = sorted(all_candidates, key=lambda x: x["score"], reverse=True)[:beam_width]

        best_seq = sequences[0]["seq"]

        caption = [
            vocab.itos[idx]
            for idx in best_seq
            if idx not in [vocab.stoi["<start>"], vocab.stoi["<end>"]]
        ]

    return " ".join(caption)


def generate_caption_with_attention(encoder, decoder, image, vocab, device, max_len=20):
    encoder.eval()
    decoder.eval()

    with torch.no_grad():
        image = image.to(device).unsqueeze(0)
        features = encoder(image)

        h = torch.zeros(1, decoder.lstm.hidden_size).to(device)
        c = torch.zeros(1, decoder.lstm.hidden_size).to(device)

        inputs = torch.tensor([vocab.stoi["<start>"]]).to(device)

        caption = []
        attention_maps = []

        for _ in range(max_len):
            embedding = decoder.embedding(inputs)

            context, alpha = decoder.attention(features, h)

            lstm_input = torch.cat((embedding.squeeze(1), context), dim=1)

            h, c = decoder.lstm(lstm_input, (h, c))

            output = decoder.fc(h)

            predicted = output.argmax(1)

            word = vocab.itos[predicted.item()]

            if word == "<end>":
                break

            caption.append(word)
            attention_maps.append(alpha.cpu().tolist())

            inputs = predicted

    return caption, attention_maps