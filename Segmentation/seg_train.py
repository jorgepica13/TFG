import sys, os
# change directory
# %cd '/mnt/homeGPU/jpicado/TFG/segmentation/'
# Let's import the python files to have access to its functions and Classes
path_to_module='/mnt/homeGPU/jpicado/TFG/segmentation/'
sys.path.append(os.path.abspath(path_to_module))
import seg_datasets, seg_engine, seg_model, seg_config_multiclass, seg_utils

import torch
import torch.nn as nn
import os

seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True

lr = 1e-4
imgsz = 256
batch = 32
epochs = 40
scheduler = True

if __name__ == '__main__':
    # Create a directory with the model name for outputs.
    out_dir = '/mnt/homeGPU/jpicado/TFG/segmentation/output/'
    out_dir_valid_preds = os.path.join(out_dir, 'valid_preds')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(out_dir_valid_preds, exist_ok=True)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('DEVICE: ', device)
    model = seg_model.prepare_model(num_classes=len(seg_config_multiclass.ALL_CLASSES)).to(device)
    # Total parameters and trainable parameters.
    total_params = sum(p.numel() for p in model.parameters())
    print(f"{total_params:,} total parameters.")
    total_trainable_params = sum(
        p.numel() for p in model.parameters() if p.requires_grad)
    print(f"{total_trainable_params:,} training parameters.")

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    train_images, train_masks, valid_images, valid_masks = seg_datasets.get_images(
        root_path='/mnt/homeGPU/jpicado/TFG/galaxy_multiclass_seg/'    
    )

    classes_to_train = seg_config_multiclass.ALL_CLASSES

    train_dataset, valid_dataset = seg_datasets.get_dataset(
        train_images, 
        train_masks,
        valid_images,
        valid_masks,
        seg_config_multiclass.ALL_CLASSES,
        classes_to_train,
        seg_config_multiclass.LABEL_COLORS_LIST,
        img_size=imgsz
    )

    train_dataloader, valid_dataloader = seg_datasets.get_data_loaders(
        train_dataset, valid_dataset, batch_size=batch
    )

    # Initialize `SaveBestModel` class.
    save_best_model = seg_utils.SaveBestModel()
    # LR Scheduler.
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.1, verbose=True)

    EPOCHS = epochs
    train_loss, train_pix_acc = [], []
    valid_loss, valid_pix_acc = [], []
    for epoch in range (EPOCHS):
        print(f"EPOCH: {epoch + 1}")
        train_epoch_loss, train_epoch_pixacc = seg_engine.train(
            model,
            train_dataset,
            train_dataloader,
            device,
            optimizer,
            criterion,
            classes_to_train
        )
        valid_epoch_loss, valid_epoch_pixacc = seg_engine.validate(
            model,
            valid_dataset,
            valid_dataloader,
            device,
            criterion,
            classes_to_train,
            seg_config_multiclass.LABEL_COLORS_LIST,
            epoch,
            seg_config_multiclass.ALL_CLASSES,
            save_dir=out_dir_valid_preds
        )
        train_loss.append(train_epoch_loss)
        train_pix_acc.append(train_epoch_pixacc.cpu())
        valid_loss.append(valid_epoch_loss)
        valid_pix_acc.append(valid_epoch_pixacc.cpu())

        save_best_model(
            valid_epoch_loss, epoch, model, out_dir
        )

        print(f"Train Epoch Loss: {train_epoch_loss:.4f}, Train Epoch PixAcc: {train_epoch_pixacc:.4f}")
        print(f"Valid Epoch Loss: {valid_epoch_loss:.4f}, Valid Epoch PixAcc: {valid_epoch_pixacc:.4f}")
        if scheduler:
            scheduler.step()
        print('-' * 50)

    seg_utils.save_model(EPOCHS, model, optimizer, criterion, out_dir)
    # Save the loss and accuracy plots.
    seg_utils.save_plots(
        train_pix_acc, valid_pix_acc, train_loss, valid_loss, out_dir
    )
    print('TRAINING COMPLETE')