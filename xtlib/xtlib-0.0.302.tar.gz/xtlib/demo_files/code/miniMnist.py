#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# miniMnist.py: ML program for testing XT
'''
Adapted from full_miniMnist.py:
    - removed checkpointing
    - removed distributed training
    - removed all "output" type directories
    - support for menu/interaction with xt monitor
'''

import os
import sys
import math
import time
import random
import argparse
import numpy as np

print("------ miniMnist starting ------")
print("current conda=", os.getenv("CONDA_DEFAULT_ENV"))

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

from xtlib import errors
from xtlib import constants
from xtlib import file_utils

def parse_cmdline_args():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')

    parser.add_argument('--batch-size', type=int, default=64, help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=64, help='input batch size for testing (default: 64)')
    parser.add_argument('--epochs', type=int, default=4, help='number of epochs to train (default: 4)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR', help='learning rate (default: 0.01)')
    parser.add_argument('--dropout', type=float, default=0, help='dropout rate (default: 0)')
    parser.add_argument('--batch-norm', type=int, default=1, help='if =1, use batch normalization in MLP (default: 1')
    parser.add_argument('--square-mlp', type=int, default=0, help='if =1, use square MLP for last module of CNN (vs. normal MLP) (default: 0')
    parser.add_argument('--cuda', type=int, default=1, help='enables/disables use of GPU resources ')
    parser.add_argument('--seed', type=int, default=0, metavar='S', help='random seed (default: 0)')
    parser.add_argument('--save-model', action='store_true', default=False, help='For Saving the current Model')
    parser.add_argument('--gpu', type=int, default=0, help='specify which gpu to use')
    parser.add_argument('--parallel', type=int, default=0, help='when specified, will do parallel training on all gpus')
    parser.add_argument('--hour', type=int, default=0, help='pseudo hyparameter; just used as a way of tagging xt_run at submit time')
    parser.add_argument('--distributed', type=int, default=0, help='when specified, will do distributed training on all nodes')
    parser.add_argument('--data', type=str, default="data/mnist", help='where to get/store MNIST data')
    parser.add_argument('--search-api', type=float, default=0, help='should app call search API?')

    # LOGGING
    parser.add_argument('--log-interval', type=int, default=1, help='how many epochs to wait before logging training status')
    parser.add_argument('--tensorboard', type=int, default=1, help='if tensorboard logging is enabled')
    parser.add_argument('--xtlib', type=int, default=1, help='if xtlib usage is enabled')
    parser.add_argument('--env-vars', type=int, default=1, help='=1 to show name/value of all environment variables')
    parser.add_argument('--tag-job', type=int, default=0, help='set =1 to tag associated with plotted_metrics=test-acc')

    # MINI MNIST
    parser.add_argument('--train-percent', type=float, default=0.001, metavar='TrainPercent', help='percent of training samples to use (default: .001)')
    parser.add_argument('--test-percent', type=float, default=1, metavar='TestPercent', help='percent of test samples to use (default: .5)')
    parser.add_argument('--download-only', action='store_true', default=False, help='when specified, app will exit after downloading data')
    parser.add_argument('--auto-download', type=int, default=1, help='when =1, app will automatically download data if needed')
    parser.add_argument('--eval-model', type=int, default=0, help='when =1, app will skip training, load existing model, and evaluate it')

    # CNN
    parser.add_argument('--mid-conv', type=int, default=0, help='number of middle conv2d layers')
    parser.add_argument('--channels1', type=int, default=20, help='number of output channels for CNN layer 1')
    parser.add_argument('--channels2', type=int, default=50, help='number of output channels for CNN layer 2')
    parser.add_argument('--kernel-size', type=int, default=5, help='size of CNN kernel')
    parser.add_argument('--mlp-units', type=int, default=100, metavar='MU', help='number of units in the MLP layer of the model')

    # OPTIMIZER
    parser.add_argument('--optimizer', type=str, default="sgd", help='sets the optimizer for the model')
    parser.add_argument('--weight-decay', type=float, default=0, help='sets rate of weight decay for weights')
    parser.add_argument('--momentum', type=float, default=0, metavar='M', help='SGD momentum (default: 0)')
    parser.add_argument('--beta1', type=float, default=0.9, metavar='M', help='Adam beta1 param (default: 0.9)')
    parser.add_argument('--beta2', type=float, default=0.999, metavar='M', help='Adam beta2 param  (default: 0.999)')
    
    # XT TESTING 
    parser.add_argument('--raise-error', type=float, default=0, help='probability that app will intentionally raise an error')

    args = parser.parse_args()
    return args

class Mlp(nn.Module):
    '''
    MLP with specified middle layers and a RELU activation function.
    '''

    def __init__(self, in_dim, middle_dims, out_dim, batch_norm=False, dropout=0) -> None:
        super().__init__()

        next_in = in_dim
        if not isinstance(middle_dims, list):
            middle_dims = [middle_dims]

        dims = middle_dims + [out_dim]
        self.layers = nn.ModuleList()

        if batch_norm:
            self.batch_norms = nn.ModuleList()
        else:
            self.batch_norms = None

        for dim in dims:
            self.layers.append( nn.Linear(next_in, dim) )
            if batch_norm:
                self.batch_norms.append( nn.BatchNorm1d(dim) )
            next_in = dim

        self.last_layer = self.layers[-1]
        self.dropout = dropout


    def forward(self, x):
        output = x
        for i, layer in enumerate(self.layers):
            output = layer(output)

            if layer != self.last_layer:
                if self.batch_norms:
                    output = self.batch_norms[i](output)

                if self.dropout:
                    output = F.dropout(output, self.dropout)
                output = F.relu(output)
                
        return output

class SimpleCNN(nn.Module):
    def __init__(self, num_mid_conv=0, channels1=20, channels2=50, kernel_size=5, mlp_units=500, batch_norm=False, dropout=0, square_mlp=False):
        super(SimpleCNN, self).__init__()

        # input to conv1: channels=1 (grayscale), W=28, H=28
        self.conv1 = nn.Conv2d(1, channels1, kernel_size, 1)
        self.dropout = dropout

        for i in range(num_mid_conv):
            name = "conv" + str(2+i)
            convX = nn.Conv2d(channels1, channels1, kernel_size, 1, padding=2)
            setattr(self, name, convX)

        self.conv_last = nn.Conv2d(channels1, channels2, kernel_size, 1)
        self.channels2 = channels2
        self.num_mid_conv = num_mid_conv

        sz1 = 28-kernel_size+1
        assert sz1 % 2 == 0
        pool1 = sz1 // 2

        sz2 = pool1-kernel_size+1
        assert sz2 % 2 == 0
        pool2 = sz2 // 2

        self.factor = pool2*pool2*channels2
        #print("sz1=", sz1, ", sz2=", sz2, ", factor=", self.factor)
        
        self.mlp = Mlp(self.factor, mlp_units, 10, batch_norm=batch_norm, dropout=dropout)

    def forward(self, input):
        dropout = self.dropout

        # first CONV2D
        x = F.relu(self.conv1(input))

        # middle CONV2D's
        for i in range(self.num_mid_conv):
            name = "conv" + str(2+i)
            convX = getattr(self, name)
            x = F.relu(convX(x))
            if dropout:
                x = F.dropout(x, dropout)

        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv_last(x))
        if dropout:
            x = F.dropout(x, dropout)
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4*4*self.channels2)

        x = self.mlp(x)

        return F.log_softmax(x, dim=1)


class Trainer():
    def __init__(self):
        pass

    def train(self, args, model, device, optimizer, epoch):
        model.train()
        total_correct = 0
        total = 0
        steps = 0
        started = time.time()

        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            result = model(data)
            loss = F.nll_loss(result, target)
            loss.backward()
            optimizer.step()

            # compute train-acc
            pred = result.argmax(dim=1, keepdim=True) # get the index of the max log-probability
            correct = pred.eq(target.view_as(pred)).sum().item()
            total_correct += correct
            total += len(data)
            steps += 1

        elapsed = time.time() - started
        return loss.item(), total_correct/total, steps, len(data), loss, total_correct, total, elapsed    

    def test(self, args, model, device):
        test_loader = self.test_loader

        model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                result = model(data)
                test_loss += F.nll_loss(result, target, reduction='sum').item() # sum up batch loss
                pred = result.argmax(dim=1, keepdim=True) # get the index of the max log-probability
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        test_acc = correct / len(test_loader.dataset)

        print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * test_acc))

        return test_loss, test_acc

    def get_dataset(self, data_dir, train, auto_download):
        ds = datasets.MNIST(data_dir, train=train, download=auto_download, transform=transforms.Compose([
            # TENSOR transforms
            transforms.ToTensor(), 
            transforms.Normalize((0.1307,), (0.3081,)),
            ]))
        return ds

    def sample_mnist(self, data_dir, train, rand, percent, auto_download):

        # get MNIST data
        ds = self.get_dataset(data_dir, train, auto_download)

        # support previous torchvision version as well as current  (AML workaround)
        if hasattr(ds, "data"):
            data_attr = "data"
            target_attr = "targets"
        elif train:
            data_attr = "train_data"
            target_attr = "train_labels"
        else:
            data_attr = "test_data"
            target_attr = "test_labels"

        # extract data and targets
        data = getattr(ds, data_attr)
        targets = getattr(ds, target_attr)

        count = len(data)
        indexes = list(range(count))

        rand.shuffle(indexes)

        samples = int(count * percent)
        indexes = indexes[0:samples]
        
        # update data
        setattr(ds, data_attr, data[indexes])

        # update targets
        setattr(ds, target_attr, targets[indexes])

        which = "TRAIN" if train else "TEST"
        print("Sampled " + which + " data: ", len(data), ", targets=", len(targets))
        return ds

    def train_test_loop(self, xt_run, model, device, optimizer, start_epoch, live_output_test_dir, args):

        epoch_steps = 0
        total_steps = 0
        start = time.time()
        print("train_test_loop: start_epoch={} end_epoch={}, device={}\n".format(start_epoch, args.epochs + 1, device))

        epoch = start_epoch

        # allow for dynamic changing of args.epochs
        while epoch <= args.epochs:

            # train an epoch
            train_loss, train_acc, steps, data_len,  loss, total_correct, total, elapsed_call = \
                self.train(args, model, device, optimizer, epoch)

            epoch_steps += steps
            total_steps += steps

            if epoch % args.log_interval == 0:
                elapsed = time.time() - start
                steps_per_sec = epoch_steps/elapsed
                #print("{} epoch(s) training took: {:.2f} secs".format(args.log_interval, elapsed))

                self.log_stats_and_test(epoch, steps, data_len, loss, total_correct, total, model, device, 
                    xt_run, train_loss, train_acc, steps_per_sec, args)
            
                start = time.time()
                epoch_steps = 0
            
            # write something changing to live_output_test_dir
            fn = live_output_test_dir + "/progress.txt"
            with open(fn, "at") as progress_file:
                progress_file.write("total_steps: {}\n".format(total_steps))
            
            epoch += 1

    def save_model(self, model, fn):
        # ensure output dir exists
        dir = os.path.dirname(fn)
        if not os.path.exists(dir):
            os.makedirs(dir)

        torch.save(model.state_dict(), fn)

    def log_stats_and_test(self, epoch, steps, data_len, loss, total_correct, total, model, device, 
        xt_run, train_loss, train_acc, steps_per_sec, args):

        msg = 'Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tAcc: {:.6f}\tSteps: {:,}\tSteps/sec: {:.2f}'.format(
            epoch, steps * data_len, len(self.train_loader.dataset),
            100. * steps / len(self.train_loader), loss.item(), total_correct/total, steps, steps_per_sec)

        # print to console
        print(msg)

        if xt_run:
            # log TRAINING stats
            train_loss = np.float64(train_loss)   # test XT's ability to convert np floats to python
            xt_run.log_metrics({"epoch": epoch, "loss": train_loss, "acc": train_acc}, step_name="epoch", stage="train")

            # log EVAL/TEST stats half as often
            if (epoch / args.log_interval ) % 2 == 0:
                test_loss, test_acc = self.test_model_and_log_metrics(xt_run, model, device, epoch, args)

                # early stopping
                if math.isnan(test_loss):
                    xt_run.log_event("early_stopping", {"reason": "loss_is_nan"})
                    # exit without error
                    sys.exit(0)

    def test_model_and_log_metrics(self, run, model, device, epoch, args):
        # TEST the model
        test_loss, test_acc = self.test(args, model, device)
        
        # log TEST METRICS
        run.log_metrics({"epoch": epoch, "loss": test_loss, "acc": test_acc}, step_name="epoch", stage="test")

        return test_loss, test_acc

    def init_dirs(self, args):
        # set live_output_test_dir (using environment variable setting from xt)
        live_output_test_dir = os.getenv("XT_OUTPUT_DIR", "output") + "/live_output_test"
        live_output_test_dir = os.path.expanduser(live_output_test_dir)
        file_utils.ensure_dir_exists(live_output_test_dir)
        print("writing mounted output to: " + live_output_test_dir)

        # set data_dir (allowing overridden by environment variable)
        data_dir = os.getenv("XT_DATA_DIR", args.data)
        data_dir = os.path.expanduser(data_dir)

        print("getting data from: " + data_dir)

        fn_test = data_dir + "/MNIST/processed/test.pt"
        exists = os.path.exists(fn_test)
        print("fn_test={}, exists={}".format(fn_test, exists))

        fn_train = data_dir + "/MNIST/processed/training.pt"
        exists = os.path.exists(fn_train)
        print("fn_train={}, exists={}".format(fn_train, exists))

        return live_output_test_dir, data_dir

    def init_cuda(self, args):
        #---- CUDA init ----
        cuda_avail = torch.cuda.is_available()
        use_cuda = cuda_avail and args.cuda 
        gpu_count = torch.cuda.device_count()
        
        if use_cuda and not args.parallel:
            torch.cuda.set_device(args.gpu)

        print("  cuda_avail={}, GPU count={}, use_cuda={}, gpu={} ---".format(cuda_avail, gpu_count, use_cuda, args.gpu))

        if use_cuda and not cuda_avail:
            # if we cannot find a GPU, consider that a hard error (used to detect problems with seeing Philly GPUs)
            errors.env_error("CUDA not available on this platform")

        device = torch.device("cuda" if use_cuda else "cpu")
        logging = True

        return use_cuda, device, logging

    def init_xt_run(self, logging, tb_path, args):
        # init xtlib
        self.xt_run = None

        if args.xtlib and (os.getenv("XT_RUN_NAME") or tb_path):
            # access to the XTLib API
            from xtlib.run import Run as XTRun

            # create an instance of XTRunLog to log info for current run
            # we try to log to live mounted .../job32/runs/run32.3/output directory
            print("---> tb_path=", tb_path)
            self.xt_run = XTRun(xt_logging=logging, aml_logging=logging, tensorboard_path=tb_path)

            if args.tag_job:
                self.xt_run.tag_job( {"plotted_metric": "test_acc"} )

            # if "call search API" test was specified and if we are running under XT
            if args.search_api and run.run_name:
                fn_sweeps = os.path.join(file_utils.get_my_file_dir(__file__), "miniSweeps.yaml")
                sweeps = file_utils.load_yaml(fn_sweeps)
                hp_space_dict = sweeps[constants.HPARAMS_DIR]
                print("hp_space_dict=", hp_space_dict)
                search_type = "random"

                hp_set = self.xt_run.get_next_hp_set_in_search(hp_space_dict, search_type=search_type)
                print("hp_set=", hp_set)

                # apply to args
                for name, value in hp_set.items():
                    setattr(args, name, value)

    def init_random_seeds(self, args):
        #---- random seeds ----
        seed_specified = True
        if args.seed == 0:
            args.seed = int(time.time())
            seed_specified = False

        # set seed for all libraries
        self.rand = random.Random(args.seed)
        random.seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)

        if seed_specified:
            # maximize reproducibility
            torch.backends.cudnn.deterministic = True        
            torch.backends.cudnn.benchmark = False

    def init_stuff(self):
        args = self.args
        self.init_random_seeds(args)

        live_output_test_dir, data_dir = self.init_dirs(args)
        use_cuda, device, logging = self.init_cuda(args)
        print("-------------")

        tb_path = "tb_logs"
        self.init_xt_run(logging, tb_path, args)

        self.init_datasets(data_dir, use_cuda, args)

        model = self.init_model(device, args)

        return model, device, live_output_test_dir

    def init_model(self, device, args):
        print("creating CNN model...")

        model = SimpleCNN(num_mid_conv=args.mid_conv, channels1=args.channels1, channels2=args.channels2, kernel_size=args.kernel_size, 
            mlp_units=args.mlp_units, batch_norm=args.batch_norm, dropout=args.dropout, square_mlp=args.square_mlp)
            
        gpu_count = torch.cuda.device_count()

        if args.cuda==0:
            print("not using GPU (--cuda=0 was specified)")
        elif args.parallel and gpu_count > 1:
            model = nn.DataParallel(model)
            print("using PARALLEL training with {} GPUs".format(gpu_count))
        elif args.parallel:
            print("PARALLEL requested but only found {} GPUs".format(gpu_count))
        elif gpu_count > 0:
            print("using single GPU; gpu_count=", gpu_count)
        else:
            print("no GPU found; using CPU")
            
        if device:
            model.to(device)

        return model

    def init_datasets(self, data_dir, use_cuda, args):
        self.kwargs = {'num_workers': 0, 'pin_memory': True} if use_cuda else {}

        if not os.path.exists(data_dir):
            # MOUNT of data container failed; JIT download needed data
            self.xt_run.download_files_from_share("data", "mnist", data_dir)

            if not os.path.exists(data_dir):
                errors.internal_error("MNIST data dir not found: {}".format(data_dir))

        # load subset of training and test data
        ds_train = self.sample_mnist(data_dir, True, self.rand, args.train_percent, args.auto_download)
        ds_test = self.sample_mnist(data_dir, False, self.rand, args.test_percent, args.auto_download)

        self.ds_train = ds_train
        self.ds_test = ds_test

        self.train_sampler = None
        self.shuffle = True

        print("loading TRAIN data...")
        self.train_loader = torch.utils.data.DataLoader(self.ds_train, 
            batch_size=args.batch_size, shuffle=self.shuffle, sampler=self.train_sampler, **self.kwargs)

        print("loading TEST data...")
        self.test_loader = torch.utils.data.DataLoader(ds_test, 
            batch_size=args.test_batch_size, shuffle=True, **self.kwargs)

    def run(self):

        print("args=", sys.argv)
        self.args = parse_cmdline_args()
        args = self.args

        model, device, live_output_test_dir = self.init_stuff()

        start_epoch = 1
        xt_run = self.xt_run

        # log hyperparameters to xt
        self.hp_dict = {"seed":args.seed, "batch-size": args.batch_size, "epochs": args.epochs, "lr": args.lr, 
            "momentum": args.momentum, "channels1": args.channels1, "channels2": args.channels2, "kernel_size": args.kernel_size, 
                "mlp-units": args.mlp_units, "weight-decay": args.weight_decay, "optimizer": args.optimizer, 
                "mid-conv": args.mid_conv, "gpu": args.gpu, "log-interval": args.log_interval, "batch-norm": args.batch_norm, "dropout": args.dropout,
                "train_percent": args.train_percent, "test_percent": args.test_percent, "hour": args.hour}

        if xt_run:
            xt_run.log_hparams(self.hp_dict)

        # print hyperparameters
        print("hyperparameters:", self.hp_dict)
        print()

        if args.optimizer == "sgd":
            #print("using SGD optimizer")
            optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)
        elif args.optimizer == "adam":
            #print("using Adam optimizer")
            optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=[args.beta1, args.beta2])
        elif args.optimizer == "adamw":
            #print("using Adam optimizer")
            optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=[args.beta1, args.beta2])
        else:
            raise Exception("unrecognized optimizer: {}".format(args.optimizer))

        self.train_test_loop(xt_run, model, device, optimizer, 1, live_output_test_dir, args=args)

        if (args.save_model):
            model_dir = os.getenv("XT_MODEL_DIR", "models/miniMnist")
            fn_model = model_dir + "/mnist_cnn.pt"

            file_utils.ensure_dir_exists(model_dir)
            self.save_model(model, fn_model)   

        xt_run.close()

def main():
    trainer = Trainer()
    trainer.run()

if __name__ == '__main__':
    main()

