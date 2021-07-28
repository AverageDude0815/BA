import csv
from typing import List


class Values:
    def __init__(self, train_loss: list, val_loss: list, val_accuracy: list, lr_history: list):
        self.train_loss = train_loss
        self.val_loss = val_loss
        self.val_accuracy = val_accuracy
        self.lr_history = lr_history


class Settings:
    def __init__(self, dataset: str, net: str, optimizer: str, cycle: str, decay: str, lr: str, batch_size: str):
        self.dataset = dataset
        self.net = net
        self.optimizer = optimizer
        self.cycle = cycle
        self.decay = decay
        self.lr = lr
        self.batch_size = batch_size


class Labels:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.dataset = settings.dataset
        self.net = settings.net
        self.optimizer = settings.optimizer
        self.decay = self.label_decay()
        self.cycle = self.label_cycle()
        self.initial_lr = self.label_initial_lr()
        self.max_lr = self.label_max_lr()
        self.batch_size = self.label_batch_size()

    def label_decay(self) -> str:
        if self.settings.decay.split('=')[-1] == 'False':
            return 'no decay'
        if self.settings.decay.split('=')[-1] == 'False':
            return 'decay'
        if self.settings.decay.split('=')[-1] == 'maxLR':
            return 'decaying peaks'
        if self.settings.decay.split('=')[-1] == 'slope':
            return 'decaying downwards slope'
        raise ValueError('unresolved title for decay')

    def label_cycle(self) -> str:
        if self.settings.cycle == 'constantLR':
            return 'constant lr'
        else:
            return self.settings.cycle

    def label_initial_lr(self):
        if '=' in self.settings.lr:
            if '-' in self.settings.lr:
                return self.settings.lr.split('=')[-2]
            else:
                return self.settings.lr.split('=')[-1]
        raise ValueError('unresolved title for lr')

    def label_max_lr(self) -> str:
        if '-' in self.settings.lr:
            return self.settings.lr.split('-')[-1]
        elif '=' in self.settings.lr:
            return self.settings.lr.split('=')[-1]
        raise ValueError('unresolved title for lr')

    def label_batch_size(self):
        if '=' in self.settings.batch_size:
            return self.settings.batch_size.split('=')[-1]
        raise ValueError('unresolved title for batch size')


class Results:
    def __init__(self, settings: Settings, values: Values):
        self.settings = settings
        self.values = values

    def get_labels(self) -> Labels:
        return Labels(self.settings)


def open_contents(settings: Settings) -> Results:
    dataset = settings.dataset
    net = settings.net
    optimizer = settings.optimizer
    cycle = settings.cycle
    decay = settings.decay
    lr = settings.lr
    batch_size = settings.batch_size
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay
            + '/' + lr + '/' + batch_size + '/train_loss') as f:
        train_loss_helper = []
        for row in csv.reader(f):
            train_loss_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay
            + '/' + lr + '/' + batch_size + '/val_loss') as f:
        val_loss_helper = []
        for row in csv.reader(f):
            val_loss_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay
            + '/' + lr + '/' + batch_size + '/val_accuracy') as f:
        val_accuracy_helper = []
        for row in csv.reader(f):
            val_accuracy_helper.append(row)
    with open(
            dataset + '/' + net + '/' + optimizer + '/' + cycle + '/' + decay
            + '/' + lr + '/' + batch_size + '/lr_history') as f:
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
    values = Values(train_loss, val_loss, val_accuracy, lr_history)

    return Results(settings, values)


def open_all_contents(settings_list: List[Settings]) -> List[Results]:
    results = []
    for settings in settings_list:
        results.append(open_contents(settings))
    return results
