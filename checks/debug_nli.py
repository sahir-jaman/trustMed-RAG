from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/nli-deberta-v3-small")
print("Label names:", model.config.id2label)

pairs = [
    ("A man is eating pizza in a restaurant.", "A man is eating food."),         # should be ENTAILMENT
    ("A man is eating pizza in a restaurant.", "The man is sleeping at home."),  # should be CONTRADICTION
    ("Trastuzumab reduced breast cancer mortality by 33% in a meta-analysis of 13,864 women.",
     "Trastuzumab lowered breast cancer deaths."),                               # should be ENTAILMENT
]

print("\nRaw scores:")
for p, h in pairs:
    print(model.predict([(p, h)])[0], " | ", h)

print("\nWith softmax:")
for p, h in pairs:
    print(model.predict([(p, h)], apply_softmax=True)[0], " | ", h)