from clip import load, tokenize
import torch


class Image(torch.nn.Module):
    def __init__(self, model, preprocess):
        super().__init__()
        self.model = model
        self.preprocess = preprocess

    def forward(self, x):
        return self.model.encode_image(x)


class Text(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        return self.model.encode_text(x)

    def preprocess(self, x):
        return tokenize(x)[0]


class CLIP(torch.nn.Module):
    def __init__(self, name):
        super().__init__()
        model, preprocess = load(name)
        self.image = Image(model, preprocess)
        self.text = Text(model)

    def preprocess(self, r):
        out = {}
        if "brand" in r or "title" in r:
            out["text"] = self.text.preprocess(f'{r.get("brand", "")} {r.get("title", "")}')
        if "img" in r:
            out["image"] = self.image.preprocess(r['img'])
        assert out
        return out

    def forward(self, r):
        assert r
        key = next(iter(r.keys()))
        bs = r[key].shape[0]
        out = torch.zeros(bs, 1024).to(r[key].device)
        n = 0
        if 'image' in r:
            tmp = self.image.forward(r['image'])
            tmp = tmp.div(tmp.pow(2).sum(axis=1).sqrt()[:, None])
            out += tmp
            n += 1
        if 'text' in r:
            tmp = self.text.forward(r['text'])
            tmp = tmp.div(tmp.pow(2).sum(axis=1).sqrt()[:, None])
            out += tmp
            n += 1
        return out / n


class Classifier:
    def __init__(self, categories, name):
        self.categories = categories
        self.model, _ = load(name)
        self.category_vectors = \
            self.model.encode_text(torch.cat([tokenize(x) for x in categories], 0))
        self.category_vectors = self.category_vectors / self.category_vectors.norm(dim=1, keepdim=True)

    def eval(self):
        self.model.eval()

    def preprocess(self, x):
        if isinstance(x, dict):
            x = x['_outputs']['_base']['clip']
        else:
            assert isinstance(x, torch.Tensor)
        return x

    def forward(self, x):
        x = x / x.norm(dim=1, keepdim=True)
        logit_scale = self.model.logit_scale.exp()
        logits_per_image = logit_scale * x @ self.category_vectors.t()
        out = logits_per_image.softmax(dim=-1)
        return out

    def postprocess(self, x):
        pos = x.topk(1)[1].item()
        return self.categories[pos]
