import argparse, os
import tensorflow as tf
import tensorflow_datasets as tfds

IMG_SIZE = 224
BATCH = 32
AUTOTUNE = tf.data.AUTOTUNE
SAVE_DIR = "saved_model"

def preprocess(example):
    image = tf.image.resize(example["image"], (IMG_SIZE, IMG_SIZE))
    image = tf.keras.applications.mobilenet_v2.preprocess_input(tf.cast(image, tf.float32))
    label = example["label"]
    return image, label

def build_model(num_classes: int):
    base = tf.keras.applications.MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3),
                                             include_top=False, weights="imagenet")
    base.trainable = False
    x = tf.keras.layers.GlobalAveragePooling2D()(base.output)
    out = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(base.input, out)
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    return model, base

def main(args):
    ds, info = tfds.load("tf_flowers", split=["train[:80%]", "train[80%:]"], with_info=True, as_supervised=False)
    train_ds = ds[0].map(preprocess, num_parallel_calls=AUTOTUNE).shuffle(2048).batch(BATCH).prefetch(AUTOTUNE)
    val_ds   = ds[1].map(preprocess, num_parallel_calls=AUTOTUNE).batch(BATCH).prefetch(AUTOTUNE)
    num_classes = info.features["label"].num_classes

    model, base = build_model(num_classes)
    # head training
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)
    # light finetuning
    if args.finetune_epochs > 0:
        base.trainable = True
        for layer in base.layers[:-30]:
            layer.trainable = False
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                      loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])
        model.fit(train_ds, validation_data=val_ds, epochs=args.finetune_epochs)

    os.makedirs(SAVE_DIR, exist_ok=True)
    model.save(os.path.join(SAVE_DIR, 'flowers_mnv2.keras')))
    print("Saved to", os.path.join(SAVE_DIR, "flowers_mnv2"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--finetune-epochs", type=int, default=2)
    main(ap.parse_args())
