"""The demo dataset. ``seed_demo`` turns it into rows.

``LEARNER`` and ``ADMIN`` stand for the two shared demo accounts, whose emails
come from settings. Times are days before the seed runs, so the data never
goes stale.
"""

from dataclasses import dataclass
from inspect import cleandoc

from commerce.models import OrderStatus
from courses.models import CourseStatus
from enrollments.models import EnrollmentSource
from reviews.models import ReviewStatus

from . import assets

LEARNER = "demo-learner"
ADMIN = "demo-admin"

LEARNER_NAME = "Demo Learner"
ADMIN_NAME = "Demo Admin"


@dataclass(frozen=True)
class LessonSpec:
    title: str
    body: str
    preview: bool = False
    video: assets.Asset | None = None
    slides: assets.Asset | None = None
    duration_seconds: int | None = None


def lesson(title, body, **fields):
    return LessonSpec(title, cleandoc(body), **fields)


# Slugs, titles, descriptions and prices match the landing page's course preview.
COURSES = [
    {
        "slug": "foundations-of-neurolinguistics",
        "created_days_ago": 120,
        "title": "Foundations of Neurolinguistics",
        "description": "Where language sits in the brain, and how we found out.",
        "price_cents": 14900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Mapping language",
                [
                    lesson(
                        "Broca, Wernicke and the lesion method",
                        """
                        ## Two patients, one method

                        In 1861 the French surgeon **Paul Broca** examined a patient known as
                        "Tan", after the only syllable he could reliably say. Tan understood
                        much of what was said to him, but could barely speak. When he died,
                        Broca found damage in the left inferior frontal gyrus, a region now
                        called [Broca's area](https://en.wikipedia.org/wiki/Broca%27s_area).

                        Thirteen years later **Carl Wernicke** described the mirror image:
                        patients who spoke fluently but made little sense, and who struggled to
                        understand others. Their damage sat further back, in the left superior
                        temporal gyrus.

                        ## The logic of a lesion

                        The lesion method reasons from loss to function:

                        - If damage to region A impairs ability X but spares Y,
                        - and damage to region B impairs Y but spares X,
                        - then X and Y rely on at least partly separate machinery.

                        This pattern is called a **double dissociation**, and Broca's and
                        Wernicke's patients were one of the first clear examples.

                        > A lesion tells you what a region is necessary for, not everything it
                        > does.

                        The method has limits. Strokes follow blood vessels rather than
                        functional boundaries, so lesions are large and messy, and the brain
                        reorganizes after injury. Still, nearly every later method was first
                        checked against what lesions showed.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "The classical language network",
                        """
                        ## Wernicke–Lichtheim–Geschwind

                        Wernicke did more than describe a second patient. He proposed a
                        **network**: an auditory word store in the temporal lobe, a motor
                        speech store in the frontal lobe, and a pathway between them. Ludwig
                        Lichtheim extended the diagram in 1885, and Norman Geschwind revived it
                        in the 1960s.

                        The connecting pathway is the **arcuate fasciculus**, a bundle of white
                        matter that arcs around the Sylvian fissure. The model made a bold
                        prediction: cut the pathway but spare both ends, and a patient should
                        understand and speak fluently yet be unable to *repeat* what they hear.
                        That syndrome, **conduction aphasia**, turned out to exist.

                        ## What the classical model misses

                        - Comprehension isn't confined to Wernicke's area; it draws on much of
                          the temporal lobe.
                        - Broca's area contributes to syntax and working memory, not only to
                          articulation.
                        - Both hemispheres take part, especially in prosody and discourse.

                        The modern successor is the **dual-stream model** (Hickok & Poeppel,
                        2007). A ventral stream maps sound to meaning, and a dorsal stream maps
                        sound to articulation.

                        > The classical model was wrong in its details and right in its
                        > instinct: language is a network, not a spot.
                        """,
                    ),
                    lesson(
                        "How sound reaches the language areas",
                        """
                        ## From air to cortex

                        Before Wernicke's area can do anything with a word, the word has to get
                        there. This short animation follows sound from the outer ear to the
                        brain:

                        1. The eardrum and the three middle-ear bones turn pressure waves into
                           mechanical motion.
                        2. In the **cochlea**, hair cells convert that motion into electrical
                           signals, with different positions tuned to different frequencies.
                        3. The auditory nerve carries the signal through the brainstem and
                           thalamus to **primary auditory cortex** in the temporal lobe.

                        Speech-specific processing starts just beyond that point, in the
                        superior temporal gyrus and sulcus, the start of the ventral stream from
                        the previous lesson.

                        > Watch for the frequency map in the cochlea. Auditory cortex keeps the
                        > same layout, called tonotopy.

                        *Video: "Journey of Sound to the Brain", National Institute on Deafness
                        and Other Communication Disorders (NIH). Public domain, via
                        [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Journey_of_Sound_to_the_Brain.ogv).*
                        """,
                        preview=True,
                        video=assets.VIDEO,
                        duration_seconds=assets.VIDEO_DURATION_SECONDS,
                    ),
                ],
            ),
            (
                "Modern methods",
                [
                    lesson(
                        "What fMRI can and can't tell us",
                        """
                        ## Measuring blood, not thought

                        Functional MRI measures the **BOLD signal**, the change in blood
                        oxygenation that follows neural activity. Active neurons draw more
                        oxygenated blood than they need, and the magnet can detect the
                        difference.

                        That detour through blood flow shapes everything fMRI can say:

                        - **Spatial resolution** is good, around a few millimetres.
                        - **Temporal resolution** is poor: the blood response peaks about four to
                          six seconds after the activity that caused it.
                        - Results are **relative**. A typical study subtracts one condition
                          from another, such as reading real words minus reading pseudowords.

                        ## The reverse-inference trap

                        "Broca's area lit up, so participants were processing syntax" sounds
                        convincing, but most regions respond to many tasks.
                        [Poldrack (2006)](https://doi.org/10.1016/j.tics.2005.12.004) showed
                        how weak that inference usually is.

                        > fMRI tells you where a task's demands differ, not what a region is
                        > *for*.

                        The attached slides are a short textbook excerpt comparing CT, PET, MRI,
                        fMRI and EEG.

                        *Slides: "Brain Imaging", from Spielman, Jenkins & Lovett,
                        [Psychology 2e](https://openstax.org/details/books/psychology-2e)
                        (OpenStax, 2020), CC BY 4.0.*
                        """,
                        slides=assets.SLIDES,
                    ),
                    lesson(
                        "EEG and the N400",
                        """
                        ## A sentence that breaks

                        In 1980 Marta Kutas and Steven Hillyard showed people sentences one word
                        at a time. Some ended normally; some did not:

                        > He spread the warm bread with *socks*.

                        About 400 milliseconds after the odd word, the EEG showed a negative
                        deflection over the centre and back of the scalp. They called it the
                        **[N400](https://en.wikipedia.org/wiki/N400_(neuroscience))**.

                        ## What the N400 tracks

                        - It is **graded**, not all-or-nothing. Unexpected but sensible words
                          ("He spread the warm bread with *jam*" versus *butter*) produce a
                          smaller N400.
                        - It tracks how expected a word is in context, not whether the sentence
                          is grammatical.
                        - Grammatical violations produce a different, later positive wave, the
                          **P600** (Osterhout & Holcomb, 1992).

                        ## Why EEG complements fMRI

                        EEG records electrical activity directly, so it resolves events to the
                        millisecond. It localizes poorly, though, because the skull blurs the
                        signal. Used together, the two methods answer *when* and *where*.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "aphasia-and-the-damaged-brain",
        "created_days_ago": 110,
        "title": "Aphasia and the Damaged Brain",
        "description": "What losing words after a stroke reveals about how we produce them.",
        "price_cents": 12900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Kinds of aphasia",
                [
                    lesson(
                        "Fluent and non-fluent aphasia",
                        """
                        ## Three questions

                        [Aphasia](https://en.wikipedia.org/wiki/Aphasia) is a language
                        disorder caused by brain damage, most often a stroke. Clinicians
                        classify it with three questions:

                        1. Is speech **fluent**?
                        2. Is **comprehension** preserved?
                        3. Can the person **repeat** a phrase?

                        ## The main types

                        - **Broca's aphasia**: non-fluent, effortful speech with few grammatical
                          words; comprehension relatively spared.
                        - **Wernicke's aphasia**: fluent but often empty speech full of
                          substituted words; comprehension poor.
                        - **Conduction aphasia**: fluent speech and good comprehension, but
                          repetition is impaired.
                        - **Global aphasia**: severe loss across all three.
                        - **Anomic aphasia**: mostly word-finding trouble, the mildest and most
                          common end state.

                        > The categories are textbook landmarks. Most real patients sit between
                        > them, and many move from one to another as they recover.

                        Aphasia affects language, not intelligence. Someone who can't name a
                        fork still knows exactly what to do with it.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "Case notes: anomia",
                        """
                        ## The word is right there

                        **Anomia**, difficulty retrieving words, appears in almost every type of
                        aphasia. It feels like a permanent tip-of-the-tongue state.

                        Consider a composite case: a retired teacher, eight months after a left
                        hemisphere stroke, describing a picture of a kitchen:

                        > "The boy is up on the… the thing you sit on, with three legs. And the
                        > water is going over the… you wash in it."

                        ## Reading the errors

                        - **Circumlocution**: describing a word's meaning instead of saying it
                          ("the thing you sit on").
                        - **Semantic errors**: a related word in its place ("chair" for
                          *stool*).
                        - **Phonological errors**: a word with the right sounds out of order
                          ("sool" for *stool*).

                        The error type points to where retrieval broke down. Semantic errors
                        suggest trouble reaching the concept; phonological errors suggest the
                        concept was reached but its sound form wasn't.

                        A **phonemic cue**, giving the first sound, often unlocks the word, a
                        sign that the word is still stored and only access is impaired.
                        """,
                    ),
                ],
            ),
            (
                "Recovery",
                [
                    lesson(
                        "Plasticity after stroke",
                        """
                        ## Recovery has a shape

                        Most language recovery after stroke happens in the first **three to six
                        months**, the period of fastest spontaneous recovery. Improvement
                        continues for years in many people, only more slowly.

                        ## Where the recovery happens

                        Several processes overlap:

                        - **Resolution of diaschisis**: regions far from the lesion, stunned by
                          the loss of their inputs, come back online.
                        - **Perilesional recruitment**: surviving tissue around the damage takes
                          on more of the work.
                        - **Right-hemisphere involvement**: homologous right-hemisphere areas
                          become more active, especially after large left lesions.

                        > Whether right-hemisphere activity helps or hinders recovery is still
                        > debated. It may depend on the size of the lesion.

                        The best outcomes are generally linked to restoring activity in the left
                        hemisphere language network. That's part of why therapy focuses on
                        intensive, targeted practice: plasticity follows use.

                        For an accessible overview, see the
                        [NIDCD's page on aphasia](https://www.nidcd.nih.gov/health/aphasia).
                        """,
                    ),
                    lesson(
                        "Speech therapy approaches",
                        """
                        ## Two broad families

                        **Impairment-based** therapies target the damaged process itself:

                        - **Semantic feature analysis**: describing an object's category, use,
                          location and properties to strengthen the route to its name.
                        - **Melodic intonation therapy**: singing short phrases with a tapped
                          rhythm, which can help some non-fluent speakers.
                        - **Constraint-induced language therapy**: intensive practice where
                          spoken responses are required and gestures discouraged.

                        **Communication-based** therapies aim at getting the message across by
                        any means, including gesture, drawing and writing.

                        ## What the evidence says

                        A large Cochrane review
                        ([Brady et al., 2016](https://doi.org/10.1002/14651858.CD000425.pub4))
                        found that speech and language therapy improves functional
                        communication, and that higher intensity and dosage tend to help.

                        > No single approach wins for everyone. The best therapy fits the
                        > person's goals, not just the diagnosis.
                        """,
                    ),
                    lesson(
                        "Reading: living with aphasia",
                        """
                        ## The person behind the diagnosis

                        For people with aphasia, the hardest part is often not the lost words
                        but the lost conversations: friends who stop calling, and strangers who
                        assume a cognitive decline that isn't there.

                        ## Supported conversation

                        Researchers such as Aura Kagan showed that trained conversation partners
                        can reveal competence that aphasia hides. Simple techniques help:

                        - Use short sentences, and give time to respond.
                        - Ask yes/no questions when an open question stalls.
                        - Write key words down, or point to them.
                        - Confirm what you understood before moving on.

                        > "I know what I want to say. It just won't come out." A common
                        > description from people with aphasia.

                        ## Participation, not just repair

                        The **Life Participation Approach to Aphasia** sets goals around what
                        a person wants to do, such as ordering a coffee, returning to a book club
                        or managing finances, instead of only scores on naming tests.

                        The [National Aphasia Association](https://aphasia.org/) keeps a
                        directory of community groups and resources.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "the-bilingual-brain",
        "created_days_ago": 95,
        "title": "The Bilingual Brain",
        "description": "How two languages share, compete for, and reshape the same neural space.",
        "price_cents": 12900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Two languages, one brain",
                [
                    lesson(
                        "Shared and separate representations",
                        """
                        ## One network or two?

                        Early case reports described bilingual stroke patients who lost one
                        language but kept the other, which suggested separate systems. Imaging
                        studies tell a different story.

                        In proficient bilinguals, the two languages activate **largely
                        overlapping** left-hemisphere networks. Studies such as
                        [Perani et al. (1998)](https://doi.org/10.1093/brain/121.10.1841)
                        suggest that **proficiency** matters more than age of acquisition in
                        how closely the two match.

                        ## Where differences appear

                        - Less proficient second languages recruit **more** of the network,
                          especially frontal control regions, as if working harder.
                        - Differences shrink as proficiency grows.
                        - Pronunciation, acquired early or late, shows the most persistent
                          differences.

                        ## What aphasia shows

                        > In bilingual aphasia, the most common pattern is **parallel
                        > recovery**: both languages are impaired and recover together.

                        Selective loss does happen, but it is often better explained by a
                        failure of *control*, being unable to select a language, than by the
                        loss of the language itself. That idea leads to the next lesson.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "Language control and switching",
                        """
                        ## Both languages are always on

                        When a bilingual hears or reads a word, words from **both** languages
                        become active, even in a purely monolingual context. Speaking one
                        language means keeping the other in check.

                        David Green's **inhibitory control model** (1998) proposes that the
                        non-target language is actively suppressed. One prediction is
                        surprising:

                        > Switching **into** your stronger language can be slower than switching
                        > into your weaker one.

                        The stronger language needed more suppression, so it takes longer to
                        release. Meuter and Allport (1999) found exactly this asymmetric switch
                        cost.

                        ## The control network

                        Switching recruits regions involved in general cognitive control:

                        - the **left caudate nucleus**
                        - the **anterior cingulate cortex**
                        - the **dorsolateral prefrontal cortex**

                        ## The "bilingual advantage"

                        Because bilinguals practise control constantly, some researchers
                        proposed a general boost to executive function. Larger, preregistered
                        studies have mostly failed to replicate it. Treat popular claims with
                        caution.
                        """,
                    ),
                ],
            ),
            (
                "Acquisition",
                [
                    lesson(
                        "Critical periods, revisited",
                        """
                        ## The original claim

                        Eric Lenneberg (1967) argued that language must be acquired before
                        puberty, as the brain loses plasticity. Evidence came from cases of
                        late first-language exposure and from second-language learners.

                        ## The classic data

                        [Johnson and Newport (1989)](https://doi.org/10.1016/0010-0285(89)90003-0)
                        tested Chinese and Korean immigrants on English grammar. Scores fell
                        steadily with age of arrival up to about puberty, then flattened and
                        varied widely.

                        ## A sharper picture

                        A study of over 600,000 online participants
                        ([Hartshorne, Tenenbaum & Pinker, 2018](https://doi.org/10.1016/j.cognition.2018.04.007))
                        estimated that grammar-learning ability stays high until about **17 or
                        18**, then declines. To reach native-like grammar, though, learning
                        apparently has to start by about 10.

                        > Most researchers now prefer **sensitive period**: a window in which
                        > learning is easier, not a door that slams shut.

                        Different parts of language seem to have different windows. Accent is
                        the most age-sensitive; vocabulary barely seems to have one at all.
                        """,
                    ),
                    lesson(
                        "Learning a language as an adult",
                        """
                        ## Adults start faster

                        In the first months, adults usually learn **faster** than children:
                        they bring literacy, study habits and explicit reasoning. Children win
                        in the long run, mainly in pronunciation and fine grammatical
                        intuitions.

                        ## What helps

                        - **Spacing**: reviewing material over days beats cramming it into one
                          session.
                        - **Retrieval practice**: recalling a word strengthens memory more than
                          re-reading it.
                        - **Sleep**: new words become better integrated with existing vocabulary
                          after a night's sleep.
                        - **Meaningful input**: lots of comprehensible listening and reading.

                        ## The brain changes too

                        Learning a language changes the adult brain measurably. In one study,
                        military interpreters in an intensive course showed growth in the
                        hippocampus and parts of the cortex after three months
                        ([Mårtensson et al., 2012](https://doi.org/10.1016/j.neuroimage.2012.06.043)).

                        > Plasticity declines with age; it doesn't disappear.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "sign-language-and-the-brain",
        "created_days_ago": 6,
        "title": "Sign Language and the Brain",
        "description": "What signed languages show about language beyond speech.",
        "price_cents": 12900,
        "status": CourseStatus.DRAFT,
        "modules": [
            (
                "Language without sound",
                [
                    lesson(
                        "Is sign language processed like speech?",
                        """
                        ## A natural experiment

                        Signed languages such as **American Sign Language** (ASL) are full
                        human languages, with their own grammar, not gestured versions of
                        English. They use a different channel, hands and space instead of voice
                        and sound, which makes them a test case: is the left hemisphere
                        specialized for *speech*, or for *language*?

                        ## The answer: language

                        Work by Ursula Bellugi, Edward Klima and Gregory Hickok showed that
                        sign language relies on the same **left-hemisphere** regions as spoken
                        language, including Broca's and Wernicke's areas.

                        Signs have structure much like spoken words:

                        - **handshape**
                        - **location** on or near the body
                        - **movement**
                        - **palm orientation**

                        Change one, and you can change the meaning, just as swapping one sound
                        changes a spoken word.

                        > The brain cares about structure, not the channel it arrives in.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "Aphasia in signers",
                        """
                        ## A clean dissociation

                        Deaf signers who have strokes provide some of the strongest evidence for
                        left-hemisphere language specialization.

                        - **Left-hemisphere damage** produces **sign aphasia**: non-fluent or
                          fluent patterns that mirror Broca's and Wernicke's aphasia.
                        - **Right-hemisphere damage** leaves signing largely intact, even when it
                          severely impairs non-linguistic visuospatial skills such as drawing or
                          attending to the left side of space.

                        This matters because sign language is itself spatial. If the right
                        hemisphere, specialized for spatial processing, handled sign, then right
                        damage should disrupt it. Mostly it doesn't.

                        > Signers with left damage could still make meaningful **gestures** that
                        > they could no longer produce as **signs**.

                        The difference between pantomiming a key turning and signing *KEY* is
                        the difference between gesture and language, and the brain keeps them
                        apart.
                        """,
                    ),
                ],
            ),
            (
                "Space as grammar",
                [
                    lesson(
                        "Spatial syntax",
                        """
                        ## Grammar in the air

                        Signed languages use the space in front of the signer as part of their
                        grammar.

                        1. A signer introduces a person or object and assigns it a **locus**, a
                           point in space.
                        2. Later references point back to that locus, much as a pronoun refers
                           back to a noun.
                        3. **Agreement verbs** move between loci to show who did what to whom:
                           *GIVE* moving from the signer's locus toward another means "I give
                           you".

                        ## Classifiers

                        **Classifier** constructions use handshapes that stand for categories,
                        such as a flat hand for vehicles or an upright index finger for people.
                        Moving the classifier through space shows paths and positions
                        precisely.

                        > Spatial syntax recruits both hemispheres more than other parts of sign
                        > grammar do. It's one place where space and language meet.
                        """,
                    ),
                    lesson(
                        "Reading: home sign",
                        """
                        ## Language from almost nothing

                        Some deaf children grow up without access to a sign language, with
                        hearing parents who don't sign. Susan Goldin-Meadow found that many of
                        these children invent **home sign**, gesture systems with consistent
                        word order and structure that their parents' gestures lack.

                        ## A language is born

                        In the late 1970s and 1980s, new schools in Nicaragua brought deaf
                        children together for the first time. Their combined home signs became
                        **Nicaraguan Sign Language**, studied by Ann Senghas and others.

                        - The first cohort's signing was relatively simple.
                        - Younger children who joined later made it **more systematic**, for
                          example breaking continuous motion into separate path and manner
                          signs.

                        > Children don't only learn language; given the chance, they build it.

                        Read more in
                        [Senghas, Kita & Özyürek (2004)](https://doi.org/10.1126/science.1100199).
                        """,
                    ),
                ],
            ),
        ],
    },
]

LEARNERS = [
    ("priya.raman@example.com", "Priya Raman"),
    ("tomas.herrera@example.com", "Tomás Herrera"),
    ("hannah.becker@example.com", "Hannah Becker"),
    ("kwame.mensah@example.com", "Kwame Mensah"),
    ("sofia.lindqvist@example.com", "Sofia Lindqvist"),
    ("daniel.cho@example.com", "Daniel Cho"),
    ("aisha.bello@example.com", "Aisha Bello"),
    ("marcus.webb@example.com", "Marcus Webb"),
]

# (who, course slug, days ago). Each makes a paid order with one item and enrolls.
PURCHASES = [
    (LEARNER, "aphasia-and-the-damaged-brain", 75),
    (LEARNER, "foundations-of-neurolinguistics", 21),
    ("priya.raman@example.com", "foundations-of-neurolinguistics", 62),
    ("priya.raman@example.com", "the-bilingual-brain", 30),
    ("tomas.herrera@example.com", "foundations-of-neurolinguistics", 45),
    ("hannah.becker@example.com", "aphasia-and-the-damaged-brain", 50),
    ("kwame.mensah@example.com", "the-bilingual-brain", 25),
    ("sofia.lindqvist@example.com", "foundations-of-neurolinguistics", 40),
    ("sofia.lindqvist@example.com", "aphasia-and-the-damaged-brain", 38),
    ("aisha.bello@example.com", "the-bilingual-brain", 12),
    ("marcus.webb@example.com", "aphasia-and-the-damaged-brain", 22),
]

# (who, course slug, days ago, refunded by, reason). Refunds a purchase above in full.
REFUNDS = [
    (
        "sofia.lindqvist@example.com",
        "foundations-of-neurolinguistics",
        39,
        ADMIN,
        "Bought the wrong course; meant to buy Aphasia.",
    ),
]

# (who, course slug, source, days ago). Enrollments with no order.
GRANTS = [
    ("daniel.cho@example.com", "foundations-of-neurolinguistics", EnrollmentSource.MANUAL, 28),
    ("aisha.bello@example.com", "aphasia-and-the-damaged-brain", EnrollmentSource.COMP, 15),
]

# (who, course slug, days ago). Revokes an enrollment above.
REVOCATIONS = [
    ("sofia.lindqvist@example.com", "foundations-of-neurolinguistics", 39),
    ("marcus.webb@example.com", "aphasia-and-the-damaged-brain", 5),
]

# (who, course slug, days ago, status). Checkouts that never completed.
ABANDONED_CHECKOUTS = [
    ("tomas.herrera@example.com", "aphasia-and-the-damaged-brain", 10, OrderStatus.EXPIRED),
    ("marcus.webb@example.com", "the-bilingual-brain", 3, OrderStatus.EXPIRED),
]

# (who, course slug, completed lessons in curriculum order, days ago of the first and last).
COMPLETIONS = [
    (LEARNER, "aphasia-and-the-damaged-brain", 5, 72, 40),
    (LEARNER, "foundations-of-neurolinguistics", 2, 19, 9),
    ("priya.raman@example.com", "foundations-of-neurolinguistics", 5, 60, 33),
    ("priya.raman@example.com", "the-bilingual-brain", 2, 28, 20),
    ("tomas.herrera@example.com", "foundations-of-neurolinguistics", 3, 44, 14),
    ("hannah.becker@example.com", "aphasia-and-the-damaged-brain", 5, 49, 18),
    ("kwame.mensah@example.com", "the-bilingual-brain", 1, 24, 24),
    ("sofia.lindqvist@example.com", "aphasia-and-the-damaged-brain", 3, 37, 11),
    ("daniel.cho@example.com", "foundations-of-neurolinguistics", 4, 27, 6),
    ("aisha.bello@example.com", "aphasia-and-the-damaged-brain", 2, 14, 8),
    ("aisha.bello@example.com", "the-bilingual-brain", 1, 11, 11),
    ("marcus.webb@example.com", "aphasia-and-the-damaged-brain", 1, 21, 21),
]

# The demo learner's latest activity: partway through the video lesson, so the
# dashboard's Continue resumes it.
IN_PROGRESS = [
    (LEARNER, "foundations-of-neurolinguistics", "How sound reaches the language areas", 58, 1),
]

# (who, course slug, rating, body, status, days ago)
REVIEWS = [
    (
        LEARNER,
        "aphasia-and-the-damaged-brain",
        5,
        "The case notes made the categories finally click for me. The lesson on living "
        "with aphasia changed how I talk with my grandfather.",
        ReviewStatus.PUBLISHED,
        39,
    ),
    (
        "priya.raman@example.com",
        "foundations-of-neurolinguistics",
        5,
        "Clear, careful and well sourced. The EEG lesson is the best explanation of the "
        "N400 I've read.",
        ReviewStatus.PUBLISHED,
        32,
    ),
    (
        "tomas.herrera@example.com",
        "foundations-of-neurolinguistics",
        4,
        "Great overview. Module two moves a little fast if you've never seen a brain scan before.",
        ReviewStatus.PUBLISHED,
        13,
    ),
    (
        "daniel.cho@example.com",
        "foundations-of-neurolinguistics",
        4,
        "Exactly the level I wanted: rigorous without assuming a neuroscience degree.",
        ReviewStatus.PUBLISHED,
        5,
    ),
    (
        "hannah.becker@example.com",
        "aphasia-and-the-damaged-brain",
        5,
        "Moving and rigorous. I'm a nurse on a stroke ward and I've recommended it to "
        "two colleagues.",
        ReviewStatus.PUBLISHED,
        17,
    ),
    (
        "sofia.lindqvist@example.com",
        "aphasia-and-the-damaged-brain",
        4,
        "Very good. I'd love a lesson on primary progressive aphasia too.",
        ReviewStatus.PUBLISHED,
        10,
    ),
    (
        "kwame.mensah@example.com",
        "the-bilingual-brain",
        4,
        "As someone who switches between Twi and English all day, the lesson on switch "
        "costs was fascinating.",
        ReviewStatus.PUBLISHED,
        23,
    ),
    (
        "priya.raman@example.com",
        "the-bilingual-brain",
        5,
        "Honest about what the research does and doesn't show, especially on the "
        "bilingual advantage.",
        ReviewStatus.PUBLISHED,
        19,
    ),
    (
        "aisha.bello@example.com",
        "the-bilingual-brain",
        5,
        "Short lessons, real citations, no fluff.",
        ReviewStatus.PUBLISHED,
        9,
    ),
    # Hidden by an admin, so it's left out of the course's average.
    (
        "marcus.webb@example.com",
        "aphasia-and-the-damaged-brain",
        1,
        "Visit my site for cheap course bundles!!!",
        ReviewStatus.HIDDEN,
        20,
    ),
]
