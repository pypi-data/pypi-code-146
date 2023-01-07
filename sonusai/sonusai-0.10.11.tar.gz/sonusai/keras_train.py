"""sonusai keras_train

usage: keras_train [-hv] (-m MODEL) (-l VLOC) [-w KMODEL] [-e EPOCHS] [-b BATCH] [-t TSTEPS] [-p ESP] TLOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Model Python file with build and/or hypermodel functions.
    -l VLOC, --vloc VLOC            Location of SonusAI mixture database to use for validation.
    -w KMODEL, --weights KMODEL     Keras model weights file.
    -e EPOCHS, --epochs EPOCHS      Number of epochs to use in training. [default: 8].
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -p ESP, --patience ESP          Early stopping patience.

Use Keras to train a model defined by a Python definition file and SonusAI genft data.

Inputs:
    TLOC    A SonusAI mixture database directory to use for training data.
    VLOC    A SonusAI mixture database directory to use for validation data.

Results are written into subdirectory <MODEL>-<TIMESTAMP>.

"""
from sonusai import logger


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    model_name = args['--model']
    weights_name = args['--weights']
    v_name = args['--vloc']
    epochs = int(args['--epochs'])
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    esp = args['--patience']
    t_name = args['TLOC']

    import warnings
    from os import makedirs
    from os import walk
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt
    import numpy as np
    import tensorflow as tf

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        from keras import backend as kb
        from keras.callbacks import EarlyStopping

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.data_generator import KerasFromH5
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import check_keras_overrides
    from sonusai.utils import create_ts_name
    from sonusai.utils import import_keras_model
    from sonusai.utils import stratified_shuffle_split_mixid
    from sonusai.utils import reshape_outputs

    model_base = basename(model_name)
    model_root = splitext(model_base)[0]

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    output_dir = create_ts_name(model_root)
    makedirs(output_dir, exist_ok=True)
    base_name = join(output_dir, model_root)

    # Setup logging file
    create_file_handler(join(output_dir, 'keras_train.log'))
    update_console_handler(verbose)
    initial_log_messages('keras_train')

    logger.info(f'tensorflow    {tf.__version__}')
    logger.info(f'keras         {tf.keras.__version__}')
    logger.info('')

    t_mixdb = MixtureDatabase(config=t_name, show_progress=True)
    logger.info(f'Training: found {len(t_mixdb.mixtures)} mixtures with {t_mixdb.num_classes} classes from {t_name}')

    v_mixdb = MixtureDatabase(config=v_name, show_progress=True)
    logger.info(f'Validation: found {len(v_mixdb.mixtures)} mixtures with {v_mixdb.num_classes} classes from {v_name}')

    # Import model definition file
    logger.info(f'Importing {model_base}')
    model = import_keras_model(model_name)

    # Check overrides
    timesteps = check_keras_overrides(model, t_mixdb.feature, t_mixdb.num_classes, timesteps, batch_size)

    logger.info('Building model')
    try:
        hypermodel = model.MyHyperModel(feature=t_mixdb.feature,
                                        num_classes=t_mixdb.num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
        built_model = hypermodel.build_model(kt.HyperParameters())
        built_model = hypermodel.compile_default(built_model)
    except Exception as e:
        logger.exception(f'Error: build_model() in {model_base} failed: {e}')
        raise SystemExit(1)

    kb.clear_session()
    logger.info('')
    built_model.summary(print_fn=logger.info)
    logger.info('')
    logger.info(f'feature       {hypermodel.feature}')
    logger.info(f'num_classes   {hypermodel.num_classes}')
    logger.info(f'batch_size    {hypermodel.batch_size}')
    logger.info(f'timesteps     {hypermodel.timesteps}')
    logger.info(f'flatten       {hypermodel.flatten}')
    logger.info(f'add1ch        {hypermodel.add1ch}')
    logger.info(f'truth_mutex   {hypermodel.truth_mutex}')
    logger.info(f'lossf         {hypermodel.lossf}')
    logger.info(f'input_shape   {hypermodel.input_shape}')
    logger.info(f'optimizer     {built_model.optimizer.get_config()}')
    logger.info('')

    t_mixid = t_mixdb.mixids_to_list()
    v_mixid = v_mixdb.mixids_to_list()

    stratify = False
    if stratify:
        logger.info(f'Stratifying training data')
        t_mixid, _, _, _ = stratified_shuffle_split_mixid(t_mixdb, vsplit=0)

    # Use SonusAI DataGenerator to create validation feature/truth on the fly
    v_datagen = KerasFromH5(mixdb=v_mixdb,
                            mixids=v_mixid,
                            batch_size=hypermodel.batch_size,
                            timesteps=hypermodel.timesteps,
                            flatten=hypermodel.flatten,
                            add1ch=hypermodel.add1ch,
                            shuffle=False)

    # Prepare class weighting
    # class_count = np.ceil(np.array(get_class_count_from_mixids(t_mixdb, t_mixid)) / t_mixdb.feature_step_samples)
    # if t_mixdb.truth_mutex:
    #     other_weight = 16.0
    #     logger.info(f'Detected single-label mode (truth_mutex); setting other weight to {other_weight}')
    #     class_count[-1] = class_count[-1] / other_weight

    # Use SonusAI DataGenerator to create training feature/truth on the fly
    t_datagen = KerasFromH5(mixdb=t_mixdb,
                            mixids=t_mixid,
                            batch_size=hypermodel.batch_size,
                            timesteps=hypermodel.timesteps,
                            flatten=hypermodel.flatten,
                            add1ch=hypermodel.add1ch,
                            shuffle=True)

    # TODO: If hypermodel.es exists, then use it; otherwise use default here
    if esp is None:
        es = EarlyStopping(monitor='val_loss',
                           mode='min',
                           verbose=1,
                           patience=8)
    else:
        es = EarlyStopping(monitor='val_loss',
                           mode='min',
                           verbose=1,
                           patience=int(esp))

    ckpt_callback = tf.keras.callbacks.ModelCheckpoint(filepath=base_name + '-ckpt-weights.h5',
                                                       save_weights_only=True,
                                                       monitor='val_loss',
                                                       mode='min',
                                                       save_best_only=True)

    if weights_name is not None:
        logger.info(f'Loading weights from {weights_name}')
        built_model.load_weights(weights_name)

    logger.info('')
    logger.info(f'Training with no class weighting and early stopping patience = {es.patience}')
    logger.info(f'  training mixtures    {len(t_mixid)}')
    logger.info(f'  validation mixtures  {len(v_mixid)}')
    logger.info('')

    history = built_model.fit(t_datagen,
                              batch_size=hypermodel.batch_size,
                              epochs=epochs,
                              validation_data=v_datagen,
                              shuffle=False,
                              callbacks=[es, ckpt_callback])

    # Save history into numpy file
    history_name = base_name + '-history'
    np.save(history_name, history.history)
    # Note: Reload with history=np.load(history_name, allow_pickle='TRUE').item()
    logger.info(f'Saved training history to numpy file {history_name}.npy')

    # Find checkpoint file and load weights for prediction and model save
    checkpoint_name = None
    for path, dirs, files in walk(output_dir):
        for f in files:
            if "ckpt" in f:
                checkpoint_name = f

    if checkpoint_name is not None:
        logger.info('Using best checkpoint for prediction and model exports')
        built_model.load_weights(join(output_dir, checkpoint_name))
    else:
        logger.info('Using last epoch for prediction and model exports')

    # save for later model export(s)
    weight_name = base_name + '.h5'
    built_model.save(weight_name)
    with h5py.File(weight_name, 'a') as f:
        f.attrs['sonusai_feature'] = hypermodel.feature
        f.attrs['sonusai_num_classes'] = str(hypermodel.num_classes)
    logger.info(f'Saved trained model to {weight_name}')

    # Compute prediction metrics on validation data using the best checkpoint
    v_predict = built_model.predict(v_datagen, batch_size=hypermodel.batch_size, verbose=1)
    v_predict, _ = reshape_outputs(predict=v_predict, timesteps=hypermodel.timesteps)

    # Write data to separate files
    v_predict_dir = base_name + '-valpredict'
    makedirs(v_predict_dir, exist_ok=True)
    for idx, mixid in enumerate(v_mixid):
        output_name = join(v_predict_dir, v_mixdb.mixtures[mixid].name)
        indices = v_datagen.file_indices[idx]
        frames = indices.stop - indices.start
        data = v_predict[indices]
        # The predict operation may produce less data due to timesteps and batches may not dividing evenly
        # Only write data if it exists
        if data.shape[0] == frames:
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=data)

    logger.info(f'Wrote validation predict data to {v_predict_dir}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
