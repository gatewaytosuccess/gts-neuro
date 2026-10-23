"""The demo's media: each file in ``api/demo/media/`` and the S3 key it lives at."""

from dataclasses import dataclass
from pathlib import Path

MEDIA_DIR = Path(__file__).parent / "media"


@dataclass(frozen=True)
class Asset:
    filename: str
    content_type: str
    private: bool
    """Private bucket if true, thumbnail bucket otherwise."""

    @property
    def key(self):
        folder = "lessons" if self.private else "thumbnails"
        # Never a course or lesson id, and inside the folders the app's S3 user can already reach.
        return f"{folder}/demo/{self.filename}"

    @property
    def path(self):
        return MEDIA_DIR / self.filename


def thumbnail(slug):
    return Asset(f"{slug}.jpg", "image/jpeg", private=False)


THUMBNAILS = {
    slug: thumbnail(slug)
    for slug in (
        "foundations-of-neurolinguistics",
        "aphasia-and-the-damaged-brain",
        "the-bilingual-brain",
        "sign-language-and-the-brain",
    )
}
VIDEO = Asset("journey-of-sound.mp4", "video/mp4", private=True)
VIDEO_DURATION_SECONDS = 147
SLIDES = Asset("brain-imaging-openstax.pdf", "application/pdf", private=True)

ALL = [*THUMBNAILS.values(), VIDEO, SLIDES]
