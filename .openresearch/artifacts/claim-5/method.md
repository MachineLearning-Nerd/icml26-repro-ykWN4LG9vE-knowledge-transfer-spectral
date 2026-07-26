# Claim 5 method

This route targets the exact real W2S arm rather than a toy surrogate. A
seeded split selects 20,000 training and 2,000 test examples from the pinned
UTKFace revision. A frozen torchvision ResNet18 produces teacher features; a
closed-form ridge head uses exactly 1,000 labeled samples. Its predictions on
all 20,000 training images become the student targets.

The student is the official OpenAI CLIP ViT-B/32. We reconstruct only its
vision stack from the hash-pinned JIT archive and expose the 768-dimensional
pre-projection representation used by the paper. The frozen student backbone
is evaluated once, then zero-initialized linear heads are trained on teacher
labels, real labels, and one fixed permutation of teacher labels. The first
five epochs match the paper's UTKFace protocol; training continues to epoch 20
as a predeclared early-stopping audit.

The primary comparisons use paired test-image squared errors and 2,000
bootstrap resamples. The verifier independently recomputes displayed MSE
values from a text CSV and exits nonzero unless the W2S effect, intermediate
stopping effect, shuffled-label control, hashes, scale, and resource record all
pass.
