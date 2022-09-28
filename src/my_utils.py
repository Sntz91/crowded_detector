import config as cfg


def convert_tensor_to_list(x):
    return x.numpy().tolist()


def convert_yolo_preds(preds):
    """
        Input: predictions of format -- tensor([[x, y, x, y, s, l]]) 
        Output: predictions of format [{boxes: tensor, labels: tensor, scores: tensor}]
        Also translates to labels
    """
    boxes = preds[:, :4]
    labels = preds[:, 5]
    scores = preds[:, 4]

    # Translate labels
    labels = [cfg.CLASSES_YOLO[int(label.item())] for label in labels]

    filtered_boxes = []
    filtered_labels = []
    filtered_scores = []

    for box, label, score in zip(boxes, labels, scores):
        if label not in cfg.CLASSES_OF_INTEREST:
            continue
        filtered_boxes.append(convert_tensor_to_list(box))
        filtered_labels.append(label)
        filtered_scores.append(convert_tensor_to_list(score))

    return filtered_boxes, filtered_labels, filtered_scores