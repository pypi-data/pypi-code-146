import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import cv2
from keras import backend as K
from keras.preprocessing import image
from matplotlib import cm
from sklearn.metrics import roc_auc_score, roc_curve


class EvaluationMetricsDCNN:

    def __int__(self):
        pass

    def plot_acc_loss(history):
        # Plot the training accuracy and loss
        plt.figure(figsize=(8, 6))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')

        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()

    def plot_roc_curve(model, X_test, y_test, class_index):
        y_pred = model.predict(X_test)
        fpr, tpr, thresholds = roc_curve(y_test[:, class_index], y_pred[:, class_index])
        roc_auc = roc_auc_score(y_test[:, class_index], y_pred[:, class_index])
        plt.figure()
        lw = 2
        plt.plot(fpr, tpr, color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.show()

    def plot_confusion_matrix(model, x_test, y_test, classes, normalize=False, title=None, cmap=plt.cm.Blues):
        # Predict the class for each example in the test set
        y_pred = model.predict(x_test)

        # Convert the predicted and true classes to one-hot encoded arrays
        y_test = np.argmax(y_test, axis=1)
        y_pred = np.argmax(y_pred, axis=1)

        # Compute the confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        # Normalize the confusion matrix if requested
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        # Create a figure and plot the confusion matrix
        fig, ax = plt.subplots()
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        ax.figure.colorbar(im, ax=ax)

        # Set the tick marks and labels
        ax.set(xticks=np.arange(cm.shape[1]), yticks=np.arange(cm.shape[0]), xticklabels=classes, yticklabels=classes,
               title=title, ylabel='True label', xlabel='Predicted label')

        # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Loop over data dimensions and create text annotations
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt), ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

        # Display the plot
        fig.tight_layout()
        plt.show()

    def visualize_activations(model, img_path, last_conv_layer_name, class_index=None, occlusion_size=50):
        # Open image
        img = cv2.imread(img_path)
        # Re-size the image to be 224 x 224 (required by VGG16 model)
        img = cv2.resize(img, (224, 224))

        # Get the output of the last convolutional layer
        last_conv_layer = model.get_layer(last_conv_layer_name)
        grads = K.gradients(model.output[:, class_index], last_conv_layer.output)[0]
        pooled_grads = K.mean(grads, axis=(0, 1, 2))
        iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
        pooled_grads_value, conv_layer_output_value = iterate([np.array([img])])
        for i in range(512):
            conv_layer_output_value[:, :, i] *= pooled_grads_value[i]

        # Get the heatmap
        heatmap = np.mean(conv_layer_output_value, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)

        # Create a jet colormap
        jet = cm.get_cmap("jet")
        jet_heatmap = jet(heatmap)

        # Convert to RGB
        jet_heatmap = np.delete(jet_heatmap, 3, 2)
        jet_heatmap = (jet_heatmap * 255).astype(np.uint8)

        # Apply the heatmap to the original image
        superimposed_img = jet_heatmap * 0.4 + img
        superimposed_img = superimposed_img.astype(np.uint8)

        # Create the occlusion
        occlusion = np.zeros((occlusion_size, occlusion_size, 3))
        x1, y1 = (img.shape[0] - occlusion_size) // 2, (img.shape[1] - occlusion_size) // 2
        x2, y2 = x1 + occlusion_size, y1 + occlusion_size
        superimposed_img[x1:x2, y1:y2, :] = occlusion
        # Create the plot
        plt.figure(figsize=(20, 10))
        plt.subplot(1, 2, 1)
        plt.title("Activations")
        plt.imshow(superimposed_img)
        plt.subplot(1, 2, 2)
        plt.title("Activations with occlusion")
        plt.imshow(cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB))
        plt.show()

    def load_custom_model(weights_path, architecture_fn, input_shape):
        model = architecture_fn(input_shape)
        model.load_weights(weights_path)
        return model

    def visualize_occluded_regions(model, img_path, target_class_idx):
        # Load and preprocess the image
        img = image.load_img(img_path)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        # Get the output of the final convolutional layer
        final_conv_layer = model.get_layer("conv2d_13")
        get_output = K.function([model.input], [final_conv_layer.output])
        conv_outputs = get_output([x])[0]

        # Create a function to compute the gradient of the target class with respect to the output of the final convolutional layer
        target_class = np.zeros((1,))
        target_class[0] = target_class_idx
        grads = K.gradients(model.output[:, target_class_idx], final_conv_layer.output)[0]

        # Compute the mean of the gradient for each feature map
        pooled_grads = K.mean(grads, axis=(0, 1, 2))

        # Create a function to compute the output of the final convolutional layer and the mean of the gradient for each feature map
        get_output_and_grads = K.function([model.input], [conv_outputs, pooled_grads])

        # Compute the output of the final convolutional layer and the mean of the gradient for each feature map
        conv_outputs, pooled_grads = get_output_and_grads([x])

        # Multiply each feature map by the corresponding weight in the pooled gradients
        for i in range(conv_outputs.shape[-1]):
            conv_outputs[:, :, i] *= pooled_grads[i]

        # Sum the feature maps to obtain the heatmap
        heatmap = np.sum(conv_outputs, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)

        # Resize the heatmap
        heatmap = cv2.resize(heatmap, (img.size[1], img.size[0]))

        # Create a jet colormap
        jet = plt.get_cmap("jet")

        # Convert the heatmap to RGB
        heatmap = jet(heatmap)
        heatmap = np.delete(heatmap, 3, 2)

        # Superimpose the heatmap on the original image
        superimposed_img = heatmap * 0.4 + img
        plt.title("Occluded regions")
        plt.imshow(superimposed_img)

    def visualize_activated_regions(model, img_path):
        # Load and preprocess the image
        img = image.load_img(img_path)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        # Get the output of the final convolutional layer
        final_conv_layer = model.get_layer("conv2d_13")
        get_output = K.function([model.input], [final_conv_layer.output])
        conv_outputs = get_output([x])[0]

        # Create a function to compute the gradient of the output of the final convolutional layer with respect to the input image
        grads = K.gradients(final_conv_layer.output, model.input)[0]

        # Compute the mean of the gradient for each feature map
        pooled_grads = K.mean(grads, axis=(0, 1, 2))

        # Create a function to compute the output of the final convolutional layer and the mean of the gradient for each feature map
        get_output_and_grads = K.function([model.input], [conv_outputs, pooled_grads])

        # Compute the output of the final convolutional layer and the mean of the gradient for each feature map
        conv_outputs, pooled_grads = get_output_and_grads([x])

        # Multiply each feature map by the corresponding weight in the pooled gradients
        for i in range(conv_outputs.shape[-1]):
            conv_outputs[:, :, i] *= pooled_grads[i]

        # Sum the feature maps to obtain the heatmap
        heatmap = np.sum(conv_outputs, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)

        # Resize the heatmap
        heatmap = cv2.resize(heatmap, (img.size[1], img.size[0]))

        # Create a jet colormap
        jet = plt.get_cmap("jet")

        # Convert the heatmap to RGB
        heatmap = jet(heatmap)
        heatmap = np.delete(heatmap, 3, 2)

        # Superimpose the heatmap on the original image
        superimposed_img = heatmap * 0.4 + img
        plt.imshow(superimposed_img)
        plt.title("Activated regions")
        plt.show()

    # def visualize_class_activation(model, img_path, class_idx):
    #     # Load the image and resize it to the input size of the model
    #     img = image.load_img(img_path, target_size=(224, 224))
    #     x = image.img_to_array(img)
    #     x = np.expand_dims(x, axis=0)
    #
    #     # Normalize the input
    #     x /= 255.
    #
    #     # Get the output of the final convolutional layer
    #     final_conv_layer = model.get_layer("block5_conv3")
    #     get_output = K.function([model.layers[0].input], [final_conv_layer.output])
    #     [conv_outputs] = get_output([x])
    #
    #     # Get the weights of the last dense layer
    #     class_weights = model.layers[-1].get_weights()[0]
    #
    #     # Compute the class activation map
    #     cam = np.dot(conv_outputs[0], class_weights[:, class_idx])
    #     cam = np.maximum(cam, 0)
    #     cam /= cam.max()
    #
    #     # Display the original image
    #     plt.figure(figsize=(10, 10))
    #     plt.imshow(img)
    #     plt.axis("off")
    #
    #     # Create a heatmap of the class activation
    #     heatmap = cv2.resize(cam, (img.size[0], img.size[1]))
    #     heatmap = np.uint8(255 * heatmap)
    #     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    #     superimposed_img = heatmap * 0.4 + img
    #     plt.imshow(superimposed_img)
    #     plt.axis("off")
    #     plt.title("Activated regions")
    #     plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
