import csv


def open_contents(dataset, net, optimizer, cycle, decay, lr, batch_size):
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay + '/' + lr + '/' + batch_size + '/train_loss') as f:
        train_loss_helper = []
        for row in csv.reader(f):
            train_loss_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay + '/' + lr + '/' + batch_size + '/val_loss') as f:
        val_loss_helper = []
        for row in csv.reader(f):
            val_loss_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay + '/' + lr + '/' + batch_size + '/val_accuracy') as f:
        val_accuracy_helper = []
        for row in csv.reader(f):
            val_accuracy_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay + '/' + lr + '/' + batch_size + '/lr_history') as f:
        lr_history_helper = []
        for row in csv.reader(f):
            lr_history_helper.append(row)

    train_loss = list(map(float, train_loss_helper[0]))
    val_loss = list(map(float, val_loss_helper[0]))
    val_accuracy = list(map(float, val_accuracy_helper[0]))
    try:
        lr_history = list(map(float, lr_history_helper[0]))
    except ValueError:
        lr_history = []

    return train_loss, val_loss, val_accuracy, lr_history