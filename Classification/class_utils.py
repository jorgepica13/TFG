import torch
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

# Function to save the trained model to disk.
def save_model(epochs, model, optimizer, criterion):
    torch.save({
                'epoch': epochs,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': criterion,
                }, '/mnt/homeGPU/jpicado/TFG/classification/outputs/model.pth')


# Function to save the loss and accuracy plots to disk.
def save_plots(train_acc, valid_acc, train_loss, valid_loss):
    # accuracy plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_acc, color='green', linestyle='-', 
        label='train accuracy'
    )
    plt.plot(
        valid_acc, color='blue', linestyle='-', 
        label='validation accuracy'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('/mnt/homeGPU/jpicado/TFG/classification/outputs/accuracy.png')
    
    # loss plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_loss, color='orange', linestyle='-', 
        label='train loss'
    )
    plt.plot(
        valid_loss, color='red', linestyle='-', 
        label='validation loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('/mnt/homeGPU/jpicado/TFG/classification/outputs/loss.png')