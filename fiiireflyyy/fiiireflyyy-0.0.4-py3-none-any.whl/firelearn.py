import os
import pathlib
import pickle
import shutil
import sys
from random import randint

import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers
from keras.models import Sequential
from matplotlib import transforms
from matplotlib.collections import PathCollection
from matplotlib.legend_handler import HandlerPathCollection, HandlerLine2D
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from umap import UMAP

from fiiireflyyy import firefiles as ff


def k_fold_cross_validation(k_fold, x, y, clf=None, loading=False, clf_path=''):
    """
    DEPRECATED - Compute a K-fold cross validation method.

    :param k_fold: Number of folds to split the dataset
    :param x: Features dataset
    :param y: target dataset
    :param clf: classifier object, if loading is False.
    :param clf_path: path of a classifier object, if loading is True.
    :param loading: Whether to load a classifier object from path or not.
    :return: k-fold scores, accuracy
    """
    if len(x) != len(y):
        raise ValueError("Features and Targets do not have the same length.")

    data_len = len(y)

    if loading:
        if clf_path == '':
            raise ValueError('No classifier path specified.')
        else:
            clf = pickle.load(open(clf_path, "rb"))
    elif clf is None:
        raise ValueError("no classifier object specified.")

    ori_x_train, ori_x_test, ori_y_train, ori_y_test = train_test_split(x, y, test_size=0.3)
    train_len = len(ori_y_train)
    test_len = len(ori_y_test)
    local_scores = []
    step = int(train_len / k_fold)
    clf.fit(ori_x_train, ori_y_train)
    for k in range(0, train_len - step, step):
        x_train_split = ori_x_train.iloc[k:k + step]
        y_train_split = ori_y_train.iloc[k:k + step]
        y_test_split = pd.concat([ori_y_test.iloc[0:k], ori_y_test.iloc[k + step:data_len]])
        x_test_split = pd.concat([ori_x_test.iloc[0:k], ori_x_test.iloc[k + step:data_len]])
        # clf.fit(x_train_split, y_train_split)
        local_scores.append(clf.score(x_test_split, y_test_split))

    return local_scores


def generate_classes(data_dir, destination, targets):
    """
    Generate a specific folder structure for Keras models by isolating classes as different folders.

    :param data_dir:
    :type data_dir: str
    :param destination: Where to generate the classes folders
    :type destination: str
    :param targets: the different classes to use
    :type targets: str
    :return:
    """
    ff.verify_dir(destination)
    files = ff.get_all_files(data_dir)

    # Creating directories architecture for keras model
    for target in targets:
        ff.verify_dir(os.path.join(destination, target))

        for file in files:
            if target in file:
                shutil.copy2(file, os.path.join(destination, target))


def basic_keras(model_spec, src, dst, img_size, epochs=10, visualize=False, saving=True):
    """
    Compute a basic Keras model for a images binary classification problem.

    :param model_spec: the name of the model. Identical to the root folder that will contain the model.
    :type model_spec: str
    :param src: Where to find the data.
    :type src: str
    :param dst: Where to save the sorted data
    :type dst: str
    :param img_size: the size of the image.
    :type img_size: tuple[int]
    :param epochs: The number of epochs of the model. Default at 10.
    :param visualize: To visualize the model's results
    :type visualize: bool
    :param saving: To save the model's results
    :type saving: bool
    :return:
    """
    # generate_classes(src, dst, targets=['INF', 'NI'])
    # Getting the dataset

    data_dir = pathlib.Path(dst)
    image_count = len(list(data_dir.glob('*.png')))
    print(image_count)

    # loading data
    batch_size = 8
    img_height = img_size[0]
    img_width = img_size[1]

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset='training',
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset='validation',
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    class_names = train_ds.class_names
    print(class_names)

    # Visualizing data
    if visualize:
        plt.figure(figsize=(10, 10))
        for images, labels in train_ds.take(1):
            for i in range(9):
                ax = plt.subplot(3, 3, i + 1)
                plt.imshow(images[i].numpy().astype("uint8"))
                plt.title(class_names[labels[i]])
                plt.axis("off")
        plt.show()

    for image_batch, labels_batch in train_ds:
        print(image_batch.shape)
        print(labels_batch.shape)
        break

    # Configure the dataset for performance

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(
        1000)  # .prefetch(buffer_size=AUTOTUNE)  # Once loaded, keep the pictures in memory
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)  # Overlaps data preprocessing/model execution while training

    # Data augmentation
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal_and_vertical",
                              input_shape=(img_height,
                                           img_width,
                                           3)),
            layers.RandomRotation(1.0),
            layers.RandomZoom(0.5),
        ]
    )

    # Basic Keras model
    num_classes = len(class_names)
    model = Sequential([
        data_augmentation,
        layers.Rescaling(1. / 255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, name="outputs")
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    # Train the model

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    # Visualize training
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')

    save_path = os.path.join(os.path.join(pathlib.Path(dst).parent.parent.absolute(), "RESULTS"), model_spec,
                             "training validation acc loss.png")
    ff.verify_dir(os.path.join(os.path.join(pathlib.Path(dst).parent.parent.absolute(), "RESULTS"), model_spec))
    if saving:
        plt.savefig(save_path)
    if visualize:
        plt.show()
    plt.close()


def keras_tutorial():
    """
    A tutorial use of keras model for image multiclass classification

    :return:
    """
    # downloading the test dataset
    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
    data_dir = pathlib.Path(data_dir)
    image_count = len(list(data_dir.glob('*/*.jpg')))

    # loading data using keras
    batch_size = 32
    img_height = 180
    img_width = 180

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    class_names = train_ds.class_names
    print(class_names)

    # Visualizing data
    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
    plt.show()

    for image_batch, labels_batch in train_ds:
        print(image_batch.shape)
        print(labels_batch.shape)
        break

    # Configure the dataset for performance

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)  # Once loaded, keep the pictures in memory
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)  # Overlaps data preprocessing/model execution while training

    # Data augmentation
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal",
                              input_shape=(img_height,
                                           img_width,
                                           3)),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
        ]
    )

    # Basic Keras model
    num_classes = len(class_names)
    model = Sequential([
        data_augmentation,
        layers.Rescaling(1. / 255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, name="outputs")
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    # Train the model
    epochs = 15
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    # Visualize training
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    # Predict on new data
    sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
    sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)

    img = tf.keras.utils.load_img(
        sunflower_path, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )


def train_RFC_from_dataset(dataset: pd.DataFrame, savepath=""):
    """
    train_model_from_dataset(dataset, model_save_path="", save=False, scores=True):

        Train a Random Forest Classifier model from an already formatted dataset.

        Parameters
        ----------
        dataset : pandas Dataframe
            a pandas Dataframe where each row is an entry for a machine
            learning model. Has a last column as 'target' containing
            the target value for each entry.

        savepath: str, optional, default:''
            name of the saved file. If empty, does not save the file.

            .. versionadded:: 1.0.0

        Returns
        -------
        out : tuple of size (1, 2).
            The first element is a trained random forest classifier.
            The second is its scores.
    """

    clf = RandomForestClassifier(n_estimators=1000)
    X = dataset[dataset.columns[:-1]]
    y = dataset["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    clf.fit(X_train, y_train)
    if savepath:
        pickle.dump(clf, open(savepath, "wb"))
    return clf, clf.score(X_test, y_test)


def get_top_features_from_trained_RFC(clf, percentage=0.05, show=False, save=False, title="", savepath=""):
    """
        get_features_of_interest_from_trained_model(clf, percentage=0.05, show=False, save=False, title=""):

            select to top n% feature sorted by highest importance, of a trained Random Forest Classtifier model.

            Parameters
            ----------
            clf : RandomForestClassifier
                a trained model

            percentage: float, optional, default: 0.05
                proportion of the most important features to keep

            show: bool, optional, default: False
                Whether to show a plot of the model feature importance or not.

            save: bool, optional, default: False
                Whether to save a plot of the model feature importance or not.

            title: str, optional, default: ''
                the title to give the plot and name of the resulting file if save if True.

            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.

            Returns
            -------
            out : tuple of lists
                first element: list of the indexes of the most important features
                second element: importance (values) corresponding to the indexes.
        """
    importances_over_iterations = []
    for i in range(10):
        mean = np.mean([tree.feature_importances_ for tree in clf.estimators_], axis=0)

        importances_over_iterations.append(mean)

    arrays = [np.array(x) for x in importances_over_iterations]
    mean_importances_over_iterations = [np.mean(k) for k in zip(*arrays)]
    std_arrays = [np.array(x) for x in importances_over_iterations]
    std_importances_over_iterations = [np.std(k) for k in zip(*std_arrays)]

    low_std = []
    for i in range(len(mean_importances_over_iterations)):
        low_std.append(mean_importances_over_iterations[i] - std_importances_over_iterations[i])
    high_std = []
    for i in range(len(mean_importances_over_iterations)):
        high_std.append(mean_importances_over_iterations[i] + std_importances_over_iterations[i])

    hertz = []
    factor = 5000 / 300
    for i in range(300):
        hertz.append(int(i * factor))
    n = int(percentage * len(mean_importances_over_iterations))
    idx_foi = sorted(range(len(mean_importances_over_iterations)),
                     key=lambda i: mean_importances_over_iterations[i], reverse=True)[:n]

    plt.bar([x for x in range(300)], mean_importances_over_iterations, color="blue", )

    xticks = [x for x in range(0, 300, 50)]
    new_ticks = [hertz[x] for x in xticks]
    xticks.append(300)
    new_ticks.append(5000)
    plt.xticks(xticks, new_ticks)
    plt.ylabel("Relative importance [AU]")
    plt.xlabel("Frequency-like features [Hz]")
    plt.title(title)
    if save:
        plt.savefig(savepath)
    # plt.fill_between(hertz, low_std, high_std, facecolor="blue", alpha=0.5)
    if show:
        plt.show()
    plt.close()
    return idx_foi, mean_importances_over_iterations


def test_model(clf, dataset: pd.DataFrame, training_targets: tuple, verbose=False, show=True, testing_targets=(), iterations=10,
               commentary="", savepath=""):
    """
        test_model(clf, dataset, training_targets, verbose=False, show=True, testing_targets=(), save=False, commentary=""):

            Test an already trained Random forest classifier model,
            resulting in a confusion matrix. The test can be done
            on targets_labels different from the targets_labels used for training
            the model.

            Parameters
            ----------
            clf: RandomForestClassifier
                the trained model.
            dataset:  pandas Dataframe.
                Dataframe containing the data used for testing the
                model. The rows are the entries, and the columns are
                the features on which the model has been trained.
                The last column is 'status' containing the labels
                of the targets_labels for each entry.
            training_targets: tuple of str
            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.


    """
    if not testing_targets:
        testing_targets = training_targets

    CORRESPONDANCE = {}
    target_id = 0
    for t in training_targets:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1
    for t in testing_targets:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1

    print(CORRESPONDANCE)
    X = dataset[dataset.columns[:-1]]
    y = dataset["label"]

    if verbose:
        progress = 0
        sys.stdout.write(f"\rTesting model: {progress}%")
        sys.stdout.flush()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # get predictions and probabilities
    all_matrixes = []
    all_probability_matrixes = []
    title = f"train {training_targets}-test {testing_targets} {commentary} iter={iterations}"
    for iters in range(iterations):
        matrix = np.zeros((len(training_targets), len(testing_targets)))
        probabilities_matrix = np.empty((len(training_targets), len(testing_targets)), dtype=object)

        # Initializing the matrix containing the probabilities
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                probabilities_matrix[i][j] = []

        # Making predictions and storing the results in predictions[]
        predictions = []
        for i in X_test.index:
            row = X_test.loc[i, :]
            y_pred = clf.predict([row])[0]
            proba_class = clf.predict_proba([row])[0]
            predictions.append((y_pred, proba_class))

        #
        targets = []
        for i in y_test.index:
            targets.append(y_test.loc[i])
        # Building the confusion matrix
        for i in range(len(targets)):
            y_true = targets[i]
            y_pred = predictions[i][0]
            y_proba = max(predictions[i][1])
            matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]] += 1

            probabilities_matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]].append(y_proba)
        mean_probabilities = np.zeros((len(training_targets), len(testing_targets)))
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                mean_probabilities[i][j] = np.mean(probabilities_matrix[i][j])
        all_matrixes.append(matrix)
        all_probability_matrixes.append(mean_probabilities)

    mixed_labels_matrix = np.empty((len(training_targets), len(testing_targets))).tolist()
    mean_probabilities_matrix = np.empty((len(training_targets), len(testing_targets)))
    overall_matrix = np.mean(np.array([i for i in all_matrixes]), axis=0)
    overall_probabilities = np.mean(np.array([i for i in all_probability_matrixes]), axis=0)

    # averaging the probabilities
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            mean_probabilities_matrix[i][j] = np.mean(overall_probabilities[i][j])

    # mixing count and probabilities for displaying
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            np.nan_to_num(overall_matrix[i][j])
            np.nan_to_num(mean_probabilities_matrix[i][j])
            mixed_labels_matrix[i][j] = str(int(overall_matrix[i][j])) + "\nCUP=" + str(
                round(mean_probabilities_matrix[i][j], 3))

    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(7 / 4 * len(testing_targets), 6 / 4 * len(training_targets)))

    fig.suptitle("")
    sns.heatmap(ax=ax, data=overall_matrix, annot=mixed_labels_matrix, fmt='')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("The input is classified as")
    ax.set_xlabel("The input is")
    ax.set_xticks([CORRESPONDANCE[x] + 0.5 for x in testing_targets], testing_targets)
    ax.set_yticks([CORRESPONDANCE[x] + 0.5 for x in training_targets], training_targets)
    plt.tight_layout()

    if savepath:
        plt.savefig(savepath)
    if show:
        plt.show()
    plt.close()

    # all_metrics.append(((positive_class, negative_class), (tp, tn, fp, fn)))


def fit_pca(dataframe: pd.DataFrame, n_components=3):
    """
    fit a Principal Component Analysis and return its instance and dataset.

    Parameters
    ----------
    dataframe: DataFrame
        The data on which the pca instance has to be fitted.
    n_components: int, optional, default: 3
        The number of components for the PCA instance.

    Returns
    -------
    out: tuple of shape (1, 3)
        The first element is the PCA instance. The second
        element is the resulting dataframe. The third is the
        explained variance ratios.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    pca = PCA(n_components=n_components)
    principalComponent = pca.fit_transform(x)
    principal_component_columns = [f"principal component {i + 1}" for i in range(n_components)]

    principal_tahyna_Df = pd.DataFrame(data=principalComponent
                                       , columns=principal_component_columns)

    principal_tahyna_Df["label"] = dataframe["label"]

    return pca, principal_tahyna_Df, pca.explained_variance_ratio_


def apply_pca(pca, dataframe):
    """
    apply_pca(pca, dataframe):

        Transform data using an already fit PCA instance.

        Parameters
        ----------
        pca: PCA instance
            The fitted PCA instance from what the data will
            be transformed.
        dataframe: DataFrame
            The data to transform using an already fitted PCA.
            Must have a 'label' column.

        Returns
        -------
        out: DataFrame
            The transformed data.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    transformed_ds = pca.transform(x)
    transformed_df = pd.DataFrame(data=transformed_ds,
                                  columns=[f"principal component {i + 1}" for i in range(transformed_ds.shape[1])])
    transformed_df['label'] = dataframe['label']
    return transformed_df


def confidence_ellipse(x, y, ax, n_std=3.0, color='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    color : str
        color of the ellipsis.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      color=color, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def plot_pca(dataframe: pd.DataFrame, n_components=3, show=True, commentary="T=48H", points=True,
             metrics=False, savedir=""):
    """
    plot the result of PCA.

    Parameters
    ----------
    dataframe: DataFrame
        The data to plot. Must contain a 'label' column.
    n_components: int, optional, default: 3
        Number of principal components. Also, teh dimension
        of the graph. Must be equal to 2 or 3.
    show: bool, optional, default: True
        Whether to show the plot or not.
    save: bool, optional, default: False
        Whether to save the plot or not.
    commentary: str, optional, default: "T=48H"
        Any specification to include in the file name while saving.
    points: bool, optional, default: True
        whether to plot the points or not.
    metrics: bool, optional, default: False
        Whether to plot the metrics or not
    savedir: str, optional, default: ""
        Directory where to save the resulting plot, if not empty.
    """
    targets = (sorted(list(set(dataframe["label"]))))
    colors = ['r', 'g', 'b', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))

    if n_components == 2:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel(f'PC-1', fontsize=20)
        plt.ylabel(f'PC-2', fontsize=20)
        plt.title(f"Principal Component Analysis for TAHV infection", fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            if points:
                alpha = 1
                if metrics:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if metrics:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)

        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)

        plt.legend(prop={'size': 15}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    elif n_components == 3:
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.set_xlabel(f'PC-1', fontsize=20)
        ax.set_ylabel(f'PC-2', fontsize=20)
        ax.set_zlabel(f'PC-3', fontsize=20)
        plt.title(f"Principal Component Analysis for TAHV infection", fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            z = dataframe.loc[indicesToKeep, 'principal component 3']
            ax.scatter3D(x, y, z, c=color, s=10)
        plt.legend(targets, prop={'size': 15})
        plt.title(f"Principal Component Analysis for TAHV infection", fontsize=20)

    if savedir:
        if commentary:
            plt.savefig(os.path.join(savedir, f"PCA n={n_components} t={targets} {commentary}.png"))
        else:
            plt.savefig(os.path.join(savedir, f"PCA n={n_components} t={targets}.png"))

    if show:
        plt.show()
    plt.close()


def fit_umap(dataframe, n_components=3):
    """
    fit a Uniform Manifold Approximated Projection and return its instance and dataset.

    Parameters
    ----------
    dataframe: DataFrame
        The data on which the umap instance has to be fitted.
        Contains a column 'label'.
    n_components: int, optional, default: 3
        The number of components for the UMAP instance.

    Returns
    -------
    out: tuple of shape (1, 2)
        The first element is the UMAP instance. The second
        element is the resulting dataframe.
    """
    # Configure UMAP hyperparameters
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    reducer = UMAP(n_neighbors=100,
                   # default 15, The size of local neighborhood (in terms of number of neighboring sample points) used for manifold approximation.
                   n_components=n_components,  # default 2, The dimension of the space to embed into.
                   metric='euclidean',
                   # default 'euclidean', The metric to use to compute distances in high dimensional space.
                   n_epochs=1000,
                   # default None, The number of training epochs to be used in optimizing the low dimensional embedding. Larger values result in more accurate embeddings.
                   learning_rate=1.0,  # default 1.0, The initial learning rate for the embedding optimization.
                   init='spectral',
                   # default 'spectral', How to initialize the low dimensional embedding. Options are: {'spectral', 'random', A numpy array of initial embedding positions}.
                   min_dist=0.1,  # default 0.1, The effective minimum distance between embedded points.
                   spread=1.0,
                   # default 1.0, The effective scale of embedded points. In combination with ``min_dist`` this determines how clustered/clumped the embedded points are.
                   low_memory=False,
                   # default False, For some datasets the nearest neighbor computation can consume a lot of memory. If you find that UMAP is failing due to memory constraints consider setting this option to True.
                   set_op_mix_ratio=1.0,
                   # default 1.0, The value of this parameter should be between 0.0 and 1.0; a value of 1.0 will use a pure fuzzy union, while 0.0 will use a pure fuzzy intersection.
                   local_connectivity=1,
                   # default 1, The local connectivity required -- i.e. the number of nearest neighbors that should be assumed to be connected at a local level.
                   repulsion_strength=1.0,
                   # default 1.0, Weighting applied to negative samples in low dimensional embedding optimization.
                   negative_sample_rate=5,
                   # default 5, Increasing this value will result in greater repulsive force being applied, greater optimization cost, but slightly more accuracy.
                   transform_queue_size=4.0,
                   # default 4.0, Larger values will result in slower performance but more accurate nearest neighbor evaluation.
                   a=None,
                   # default None, More specific parameters controlling the embedding. If None these values are set automatically as determined by ``min_dist`` and ``spread``.
                   b=None,
                   # default None, More specific parameters controlling the embedding. If None these values are set automatically as determined by ``min_dist`` and ``spread``.
                   random_state=42,
                   # default: None, If int, random_state is the seed used by the random number generator;
                   metric_kwds=None,
                   # default None) Arguments to pass on to the metric, such as the ``p`` value for Minkowski distance.
                   angular_rp_forest=False,
                   # default False, Whether to use an angular random projection forest to initialise the approximate nearest neighbor search.
                   target_n_neighbors=-1,
                   # default -1, The number of nearest neighbors to use to construct the target simplcial set. If set to -1 use the ``n_neighbors`` value.
                   # target_metric='categorical', # default 'categorical', The metric used to measure distance for a target array is using supervised dimension reduction. By default this is 'categorical' which will measure distance in terms of whether categories match or are different.
                   # target_metric_kwds=None, # dict, default None, Keyword argument to pass to the target metric when performing supervised dimension reduction. If None then no arguments are passed on.
                   # target_weight=0.5, # default 0.5, weighting factor between data topology and target topology.
                   transform_seed=42,
                   # default 42, Random seed used for the stochastic aspects of the transform operation.
                   verbose=False,  # default False, Controls verbosity of logging.
                   unique=False,
                   # default False, Controls if the rows of your data should be uniqued before being embedded.
                   )

    # Fit and transform the data
    X_trans = reducer.fit_transform(x)
    X_dimension = [f"dimension {i + 1}" for i in range(n_components)]
    transformed_df = pd.DataFrame(data=X_trans, columns=X_dimension)

    transformed_df["label"] = dataframe["label"]

    return reducer, transformed_df


def apply_umap(umap, dataframe):
    """
    Transform data using an already fit UMAP instance.

       Parameters
       ----------
       umap: UMAP instance
           The fitted PCA instance from what the data will
           be transformed.
       dataframe: DataFrame
           The data to transform using an already fitted PCA.
           Must have a 'label' column.

       Returns
       -------
       out: DataFrame
           The transformed data.
   """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    transformed_ds = umap.transform(x)
    transformed_df = pd.DataFrame(data=transformed_ds,
                                  columns=[f"dimension {i + 1}" for i in range(transformed_ds.shape[1])])
    transformed_df['label'] = dataframe['label']
    return transformed_df


def plot_umap(dataframe, n_component=3, show=True, commentary="", points=True, metrics=True, savedir=""):
    """
    plot the result of UMAP.

    Parameters
    ----------
    dataframe: DataFrame
        The data to plot. Must contain a 'label' column.
    n_components: int, optional, default: 3
        Number of principal components. Also, teh dimension
        of the graph. Must be equal to 2 or 3.
    show: bool, optional, default: True
        Whether to show the plot or not.
    save: bool, optional, default: False
        Whether to save the plot or not.
    commentary: str, optional, default: ""
        Any specification to include in the file name while saving.
    points: bool, optional, default: True
        whether to plot the points or not.
    metrics: bool, optional, default: False
        Whether to plot the metrics or not
    savedir: str, optional, default: ""
        Directory where to save the resulting plot, if not empty.
    """
    targets = (sorted(list(set(dataframe["label"]))))
    colors = ['r', 'g', 'b', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
    if n_component == 2:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel(f'PC-1', fontsize=20)
        plt.ylabel(f'PC-2', fontsize=20)
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'dimension 1']
            y = dataframe.loc[indicesToKeep, 'dimension 2']
            if points:
                alpha = 1
                if metrics:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if metrics:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)

        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)

        plt.legend(prop={'size': 15}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    if n_component == 3:
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.set_xlabel(f'dimension-1', fontsize=20)
        ax.set_ylabel(f'dimension-2', fontsize=20)
        ax.set_zlabel(f'dimension-3', fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, dataframe.columns[0]]
            y = dataframe.loc[indicesToKeep, dataframe.columns[1]]
            z = dataframe.loc[indicesToKeep, dataframe.columns[2]]
            ax.scatter3D(x, y, z, c=color, s=10, label='bla')
        plt.legend(targets, prop={'size': 15})
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)

    if savedir:
        if commentary:
            plt.savefig(os.path.join(savedir, f"UMAP n={n_component} t={targets} {commentary}.png"))
        else:
            plt.savefig(os.path.join(savedir, f"UMAP n={n_component} t={targets}.png"))

    if show:
        plt.show()
    plt.close()
