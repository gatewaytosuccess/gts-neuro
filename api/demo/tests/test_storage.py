from common import storage


def test_delete_keeps_demo_objects(s3):
    # No response queued: any S3 call fails the test.
    storage.delete("gts-private", "lessons/demo/journey-of-sound.mp4")


def test_delete_still_deletes_other_objects(s3):
    s3.add_response("delete_object", {}, {"Bucket": "gts-private", "Key": "lessons/a/b.mp4"})

    storage.delete("gts-private", "lessons/a/b.mp4")
