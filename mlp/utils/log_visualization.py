import csv
import matplotlib.pyplot as plt
import os

def log_metrics(epoch, loss, accuracy, log_file='results/logs/metrics.csv'):
    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Epoch", "Loss", "Accuracy"])

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([epoch, loss, accuracy])

def plot_metrics(log_file='results/logs/metrics.csv'):
    epochs, losses, accuracies = [], [], []

    with open(log_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            epoch, loss, accuracy = map(float, row)
            epochs.append(epoch)
            losses.append(loss)
            accuracies.append(accuracy)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, losses, label='Loss', color='blue')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(epochs, accuracies, label='Accuracy', color='green')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
