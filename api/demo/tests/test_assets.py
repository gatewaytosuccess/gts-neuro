from demo import assets


def test_keys_default_to_the_demo_folder():
    assert assets.VIDEO.key == "lessons/demo/journey-of-sound.mp4"
    assert assets.THUMBNAILS["the-bilingual-brain"].key == "thumbnails/demo/the-bilingual-brain.jpg"


def test_keys_follow_the_s3_key_folder(settings):
    settings.S3_KEY_FOLDER = "dev"

    assert assets.VIDEO.key == "lessons/dev/journey-of-sound.mp4"
    assert assets.THUMBNAILS["the-bilingual-brain"].key == "thumbnails/dev/the-bilingual-brain.jpg"
