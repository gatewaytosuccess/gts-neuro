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
    {
        "slug": "reading-and-the-brain",
        "created_days_ago": 200,
        "title": "Reading and the Brain",
        "description": "How the brain learned to read, and what dyslexia reveals about it.",
        "price_cents": 11900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Learning to see words",
                [
                    lesson(
                        "A recent invention",
                        """
                        ## Too new to be innate

                        Writing was invented about 5,000 years ago, in Mesopotamia and Egypt,
                        and for most of the time since only a small minority of people could
                        read. That is far too short for evolution to have built a brain region
                        for reading. Yet in every literate adult, reading leans on the same
                        small patch of cortex.

                        ## Neuronal recycling

                        Stanislas Dehaene's
                        [neuronal recycling hypothesis](https://en.wikipedia.org/wiki/Neuronal_recycling_hypothesis)
                        offers a way out of the puzzle. Cultural inventions such as reading and
                        arithmetic don't get new hardware. They take over circuits that evolved
                        for something close enough:

                        - The ventral visual stream already recognizes objects from any angle
                          and at any size.
                        - It is already tuned to line junctions, the T, L and Y shapes that mark
                          the edges and corners of objects.
                        - Writing systems around the world, Dehaene and colleagues argue, are
                          built largely from those same shapes.

                        On this view, scripts evolved to fit the brain, not the other way round.

                        ## The cost of learning

                        Recycling isn't free. Comparing literate and illiterate adults in
                        Portugal and Brazil,
                        [Dehaene et al. (2010)](https://doi.org/10.1126/science.1194140) found
                        that literacy strengthened responses to written words in the left visual
                        cortex, and slightly weakened responses to faces there.

                        > Reading is a borrowed skill: the brain lends it circuits built for
                        > seeing the world.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "The visual word form area",
                        """
                        ## A region for letters

                        Around 2000, imaging studies by Laurent Cohen, Stanislas Dehaene and
                        colleagues described a region in the left
                        [fusiform gyrus](https://en.wikipedia.org/wiki/Fusiform_gyrus), on the
                        underside of the brain where the occipital and temporal lobes meet, that
                        responds strongly to written words. They called it the
                        [visual word form area](https://en.wikipedia.org/wiki/Visual_word_form_area)
                        (VWFA).

                        Its responses have a few telling properties:

                        - It treats "READ" and "read" alike, although the shapes differ.
                        - It responds in much the same place whichever side of the visual field
                          the word appears in.
                        - It sits in roughly the same spot in readers of very different scripts.

                        ## Pure alexia

                        The region's importance was first shown by a lesion. In 1892 the French
                        neurologist Joseph Jules Dejerine described a man who suddenly couldn't
                        read, though he could still speak, understand and even write. He
                        couldn't read back what he had just written.

                        Patients with [pure alexia](https://en.wikipedia.org/wiki/Pure_alexia)
                        often read **letter by letter**, naming each letter before recognizing
                        the word, so the time it takes them grows with the length of the word.
                        Their damage typically involves the left ventral occipitotemporal cortex
                        or the connections feeding it.

                        > The VWFA isn't a reading center. It's a visual expert that learned
                        > letters.
                        """,
                    ),
                    lesson(
                        "Two routes to a word",
                        """
                        ## Pint and mint

                        Read these aloud: *mint*, *hint*, *pint*, *blick*. The first two follow
                        the spelling rules, the third breaks them, and the last isn't a word at
                        all, yet you read all four without effort.

                        The
                        [dual-route model](https://en.wikipedia.org/wiki/Dual-route_hypothesis_to_reading_aloud),
                        developed by Max Coltheart and colleagues, says that's because skilled
                        readers have two ways from print to sound:

                        - A **lexical route** looks the whole word up in a mental dictionary.
                          It's the only way to read irregular words like *pint* or *yacht*.
                        - A **sublexical route** converts letters to sounds by rule. It's the
                          only way to read a new word, or a nonword like *blick*.

                        ## Evidence from acquired dyslexia

                        The strongest support comes from patients who lose one route but not the
                        other after brain damage:

                        - In **surface dyslexia**, the lexical route fails. Patients read
                          regular words and nonwords, but regularize exceptions, so *pint*
                          rhymes with *mint*.
                        - In **phonological dyslexia**, the sublexical route fails. Patients
                          read familiar words, regular or not, but can't read nonwords.

                        That's a double dissociation, the same logic Broca and Wernicke used.

                        ## Not the only account

                        Connectionist models, starting with Seidenberg and McClelland (1989),
                        reproduce many of the same patterns with a single learning network, in
                        which regular and irregular words differ only in how consistent their
                        spellings are with their sounds. The debate is still open.

                        > Skilled readers switch between two systems without ever noticing.
                        """,
                    ),
                ],
            ),
            (
                "Dyslexia",
                [
                    lesson(
                        "What dyslexia is and isn't",
                        """
                        ## A difficulty with print, not with thinking

                        Developmental [dyslexia](https://en.wikipedia.org/wiki/Dyslexia) is a
                        persistent difficulty learning to read accurately and fluently, despite
                        adequate teaching and otherwise typical intelligence. Estimates of how
                        common it is range from about 5 to 10 percent of children, depending on
                        where the cut-off is drawn, because reading skill varies continuously.

                        ## Three myths

                        - **It isn't seeing letters backwards.** Young children reverse *b* and
                          *d* whether or not they're dyslexic.
                        - **It isn't low intelligence or poor effort.**
                        - **It isn't outgrown.** Adults with dyslexia often read accurately, but
                          slowly and with effort.

                        ## The phonological deficit

                        The best-supported account is that many people with dyslexia have
                        trouble with **phonological awareness**: noticing and manipulating the
                        sounds inside words. Asked to say "cat" without the /k/, or to judge
                        whether two words rhyme, they're slower and less accurate. Reading an
                        alphabet means mapping letters onto those sounds, so a weak grip on the
                        sounds makes the mapping hard to learn.

                        Imaging studies often find reduced activity while reading in
                        left-hemisphere temporoparietal regions and in the visual word form
                        area.

                        Dyslexia runs in families. Twin studies suggest genes explain a large
                        share of the variation, through many genes of small effect rather than
                        one "dyslexia gene".

                        > Dyslexia is about the sounds behind the letters more than the letters
                        > themselves.
                        """,
                    ),
                    lesson(
                        "Reading: teaching the brain to read",
                        """
                        ## What the evidence says

                        Decades of argument over how to teach reading, sometimes called the
                        "reading wars", have been largely settled by evidence. In 2000 the US
                        [National Reading Panel](https://en.wikipedia.org/wiki/National_Reading_Panel)
                        reviewed the research and found that systematic
                        [phonics](https://en.wikipedia.org/wiki/Phonics), teaching the links
                        between letters and sounds explicitly and in order, helped children
                        learn to read, especially children at risk of difficulty.

                        ## Teaching changes the brain

                        Intervention studies show the reading network responding to good
                        teaching:

                        - After intensive training in sounds and letters, children with dyslexia
                          show more activity in left-hemisphere reading areas, closer to the
                          pattern of typical readers.
                        - In adults who learn to read late in life, responses to print in the
                          visual word form area grow with their reading skill.

                        ## The earlier the better

                        Help works at any age, but it works best early. Children who struggle in
                        the first years of school read less than their classmates, so they get
                        less practice and fall further behind. Keith Stanovich called this the
                        **Matthew effect**, after a line in the Gospel of Matthew about the rich
                        getting richer.

                        > Good teaching doesn't remove the difficulty. It builds a route around
                        > it.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "how-children-learn-to-talk",
        "created_days_ago": 186,
        "title": "How Children Learn to Talk",
        "description": "How infants find words in a stream of sound, long before they speak.",
        "price_cents": 9900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Before the first word",
                [
                    lesson(
                        "Listening before birth",
                        """
                        ## The womb isn't silent

                        A fetus can hear during roughly the last trimester of pregnancy. Speech
                        reaching it through the mother's body is muffled, and high frequencies
                        are lost, but the rhythm and melody of speech, its **prosody**, get
                        through.

                        ## Newborns remember

                        Classic studies show that newborns already know something about the
                        voices and language they heard:

                        - Anthony DeCasper and William Fifer (1980) showed that newborns would
                          change their sucking pattern to hear their own mother's voice rather
                          than a stranger's.
                        - Jacques Mehler and colleagues (1988) found that four-day-old French
                          infants could tell French from Russian.
                        - Birgit Mampe, Kathleen Wermke and colleagues (2009) found that newborn
                          cries already follow the melody of the surrounding language: French
                          newborns tended to cry with a rising contour, German newborns with a
                          falling one.

                        ## Why melody first

                        Prosody marks where phrases begin and end, and which syllables carry
                        stress. Before an infant knows a single word, it gives them a rough map
                        of their language's structure, and a way to tell it apart from others.

                        > The first thing babies learn about their language is its tune.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "Citizens of the world",
                        """
                        ## Every contrast, at first

                        Languages carve up speech sounds differently. English distinguishes /r/
                        and /l/; Japanese doesn't. Hindi distinguishes two "t" sounds that
                        English speakers hear as one.

                        Janet Werker and Richard Tees (1984) tested infants from
                        English-speaking homes on contrasts from Hindi and from Nthlakampx, a
                        Salish language of British Columbia. At 6 to 8 months, most infants told
                        the sounds apart. By 10 to 12 months, few did, while Hindi- and
                        Salish-learning infants of the same age still could.

                        ## Perceptual narrowing

                        Infants start out able to hear contrasts from many languages, and over
                        the first year their perception tunes to the language around them.
                        Patricia Kuhl described infants as starting out as "citizens of the
                        world". This **perceptual narrowing** isn't only loss: sensitivity to
                        the contrasts of their own language gets sharper at the same time.

                        ## It takes a person

                        Exposure alone isn't enough. Kuhl, Tsao and Liu (2003) gave 9-month-old
                        American infants twelve short sessions with Mandarin. Infants who played
                        with a live Mandarin speaker kept the ability to hear a Mandarin
                        contrast. Infants who got the same speech from a video or an audio
                        recording didn't.

                        > Infants learn the sounds of their language from people, not just from
                        > sound.
                        """,
                    ),
                    lesson(
                        "Statistics in the stream",
                        """
                        ## Where does one word end?

                        Speech has no reliable pauses between words. Listen to an unfamiliar
                        language and it sounds like one continuous stream. So how does a baby
                        find the words?

                        ## Counting syllables

                        [Saffran, Aslin & Newport (1996)](https://doi.org/10.1126/science.274.5294.1926)
                        played 8-month-olds two minutes of a made-up language: four
                        three-syllable "words", such as *bidaku*, run together in a monotone
                        with no pauses.

                        The only cue to where words began and ended was statistical. Inside a
                        word, one syllable reliably predicted the next: *bi* was always followed
                        by *da*. Across a word boundary, the next syllable could be any of
                        several. Afterwards the infants listened longer to sequences that
                        spanned a boundary than to the real words, showing they had told them
                        apart.

                        ## Statistical learning

                        The study launched research on
                        [statistical learning](https://en.wikipedia.org/wiki/Statistical_learning_in_language_acquisition):
                        picking up on how often things occur together, without being taught.
                        Infants have since been shown to do it with tones, shapes and
                        grammar-like patterns.

                        It doesn't explain all of language. Knowing where a word ends isn't
                        knowing what it means or how to combine it with others. But it shows
                        infants are far more active listeners than they appear.

                        > Two minutes of nonsense syllables were enough for 8-month-olds to
                        > start finding words.
                        """,
                    ),
                ],
            ),
            (
                "Words and grammar",
                [
                    lesson(
                        "Babbling and first words",
                        """
                        ## Babbling is practice

                        Between about 6 and 10 months, infants start **canonical babbling**:
                        repeated consonant-vowel syllables such as *bababa* or *dadada*.
                        Clinicians watch for it, because a late start can be an early sign of
                        hearing loss.

                        [Babbling](https://en.wikipedia.org/wiki/Babbling) isn't only about the
                        mouth. Laura-Ann Petitto and Paula Marentette (1991) found that deaf
                        infants exposed to sign language babble with their hands, producing
                        rhythmic, syllable-like units drawn from the signs around them.

                        ## The first words

                        Most children say their first words around their first birthday, and
                        understand many more before then. Early vocabularies look similar across
                        languages: people (*mama*), food, animals, toys and social words (*hi*,
                        *bye*).

                        Growth is slow at first, then often speeds up in the second year. This
                        is sometimes called the **vocabulary spurt**, though researchers debate
                        whether it's a sudden change or a smooth acceleration.

                        ## Fast mapping

                        Children can learn something about a word from a single encounter. Susan
                        Carey and Elsa Bartlett (1978) introduced preschoolers to "chromium",
                        used for an olive color, in passing: bring me the chromium tray, not the
                        red one. Weeks later, many still knew something about it.

                        > Comprehension runs ahead of production: children understand words long
                        > before they say them.
                        """,
                    ),
                    lesson(
                        "Rules before they're taught",
                        """
                        ## The wug test

                        In 1958 Jean Berko Gleason showed children a drawing of a small bird:
                        "This is a wug. Now there is another one. There are two of them. There
                        are two..." Most preschoolers answered "wugs", with the right plural
                        ending, for a word they had never heard.

                        They couldn't have memorized it, so they were applying a rule. The
                        [wug test](https://en.wikipedia.org/wiki/Jean_Berko_Gleason#The_wug_test)
                        became one of the most widely used methods in child language research.

                        ## Getting worse to get better

                        Young children often say *went* correctly, and then, for a while, start
                        saying *goed*. They haven't forgotten *went*; they've discovered the
                        past-tense rule and are applying it too widely. This
                        **overregularization** gives development a U shape: correct, then
                        errors, then correct again.

                        Children's errors are systematic. They rarely make mistakes that no rule
                        would predict, which is what makes the mistakes so revealing.

                        ## Correction rarely helps

                        Parents mostly respond to what a child means, not how they said it, and
                        explicit correction often goes unheeded. Children nonetheless converge
                        on the grammar of the adults around them.

                        How they manage it, and how much of the answer is built in, divides
                        researchers. Nativist accounts in the tradition of Noam Chomsky stress
                        innate structure; usage-based accounts stress learning from the patterns
                        of what children hear. The debate is one of the longest-running in the
                        field.

                        > A child who says "goed" isn't failing to learn. They're showing their
                        > work.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "hearing-speech",
        "created_days_ago": 172,
        "title": "Hearing Speech",
        "description": "How the brain turns a pressure wave into speech, and one voice out of a crowd.",
        "price_cents": 14900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "From ear to cortex",
                [
                    lesson(
                        "From pressure wave to nerve signal",
                        """
                        ## Three stages

                        Speech arrives as tiny changes in air pressure. The ear turns them into
                        nerve signals in three stages:

                        - The **outer ear** funnels sound to the eardrum.
                        - The **middle ear**'s three small bones, the malleus, incus and stapes,
                          pass the vibration to the inner ear, concentrating it onto a much
                          smaller window.
                        - The **inner ear**'s [cochlea](https://en.wikipedia.org/wiki/Cochlea),
                          a fluid-filled spiral about the size of a pea, turns vibration into
                          nerve impulses.

                        ## A frequency map

                        Along the cochlea runs the **basilar membrane**. It's narrow and stiff
                        at the base and wider and floppier at the tip, so each frequency makes a
                        different point vibrate most: high pitches near the base, low pitches
                        near the tip. Georg von Békésy won the 1961 Nobel Prize for working out
                        this traveling wave.

                        Rows of **hair cells** on the membrane turn its movement into electrical
                        signals, carried to the brain by about 30,000 fibers of the auditory
                        nerve. This layout by frequency, called
                        [tonotopy](https://en.wikipedia.org/wiki/Tonotopy), is kept all the way
                        up to the cortex.

                        ## Why it matters for speech

                        Vowels and consonants differ in which frequencies carry their energy.
                        Because the cochlea already separates frequencies, the brain receives
                        speech as something like a running spectrogram. Hearing loss from noise
                        or age usually takes the high frequencies first, and with them
                        consonants like /s/ and /f/.

                        > By the time speech reaches the brain, the ear has already done a
                        > frequency analysis.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "The auditory cortex",
                        """
                        ## Heschl's gyrus

                        Auditory signals pass through relays in the brainstem and thalamus to
                        [primary auditory cortex](https://en.wikipedia.org/wiki/Primary_auditory_cortex),
                        on
                        [Heschl's gyrus](https://en.wikipedia.org/wiki/Transverse_temporal_gyrus),
                        tucked inside the Sylvian fissure on the upper surface of the temporal
                        lobe. Like the cochlea, it's laid out by frequency.

                        Each ear projects to both hemispheres, so damage to one side's auditory
                        cortex rarely causes deafness.

                        ## Beyond the primary area

                        Processing specific to speech begins in the surrounding cortex, along
                        the **superior temporal gyrus** and **sulcus**. These regions respond
                        more to speech than to other sounds of similar complexity, and more
                        again when the speech is intelligible.

                        Recording from electrodes placed directly on the cortex of patients
                        being prepared for epilepsy surgery, Nima Mesgarani, Edward Chang and
                        colleagues (2014) found sites in the superior temporal gyrus tuned not
                        to individual phonemes but to **phonetic features**. One site might
                        respond to all the plosives, *p*, *t*, *k*, *b*, *d* and *g*; another to
                        the fricatives, such as *s* and *f*.

                        ## Two streams

                        From here, processing splits. A ventral stream maps sound to meaning,
                        and a dorsal stream maps it to articulation, in the dual-stream model of
                        Hickok and Poeppel (2007).

                        > The superior temporal gyrus doesn't store phonemes as a list. It
                        > encodes the features they're built from.
                        """,
                    ),
                ],
            ),
            (
                "Making sense of the signal",
                [
                    lesson(
                        "Categorical perception",
                        """
                        ## A continuum heard as two

                        Say *ba* and *pa*. The main difference between them is **voice onset
                        time**: how long after the lips open the vocal folds start to vibrate.
                        For *ba* it's almost immediate; for *pa*, in English, there's a delay of
                        several tens of milliseconds.

                        A speech synthesizer can make a smooth continuum between the two, in
                        small steps. Listeners don't hear a gradual change. They hear *ba*,
                        *ba*, *ba*, then abruptly *pa*, *pa*, *pa*, with the switch for English
                        listeners at around 25 to 30 milliseconds.

                        ## Sharp at the boundary

                        Alvin Liberman and colleagues at Haskins Laboratories described this
                        [categorical perception](https://en.wikipedia.org/wiki/Categorical_perception)
                        in 1957. Its hallmark is that telling sounds apart follows how they're
                        labeled: two sounds equally far apart acoustically are easy to
                        distinguish if they straddle the boundary, and hard if they fall inside
                        one category.

                        ## Not so special

                        Liberman took categorical perception as a sign that speech is special.
                        Later work complicated that:

                        - With the right task, listeners can hear differences within a category,
                          and the brain uses them.
                        - Chinchillas place a boundary between *da* and *ta* close to where
                          English speakers do (Kuhl & Miller, 1975).
                        - Where the boundary falls depends on the listener's language.

                        > We hear speech sounds as categories, but the brain keeps more detail
                        > than we notice.
                        """,
                    ),
                    lesson(
                        "Seeing what you hear",
                        """
                        ## The McGurk effect

                        [McGurk & MacDonald (1976)](https://doi.org/10.1038/264746a0) dubbed a
                        recording of someone saying *ba* onto video of their lips saying *ga*.
                        Most viewers reported hearing *da*, a syllable that was in neither the
                        sound nor the picture.

                        The [McGurk effect](https://en.wikipedia.org/wiki/McGurk_effect) is
                        striking because knowing about it doesn't switch it off. Close your eyes
                        and you hear *ba*; open them and it's *da* again.

                        ## Vision helps in noise

                        Lipreading isn't only for people with hearing loss. Sumby and Pollack
                        (1954) found that seeing a speaker's face could improve understanding in
                        noise about as much as making the speech some 15 decibels louder.

                        ## Where sight and sound meet

                        Imaging studies point to the **superior temporal sulcus**, which
                        responds both to speech sounds and to the sight of a moving mouth, as a
                        key site where the two are combined. Visible speech even changes
                        activity in auditory cortex.

                        People vary a lot in how strongly they experience the illusion, and some
                        studies find it weaker in listeners of some languages, such as Japanese.

                        > Speech perception is multisensory: the brain listens with its eyes
                        > too.
                        """,
                    ),
                    lesson(
                        "The cocktail party problem",
                        """
                        ## One voice among many

                        In 1953 the British engineer Colin Cherry named the
                        [cocktail party problem](https://en.wikipedia.org/wiki/Cocktail_party_effect):
                        how do we follow one speaker when several talk at once?

                        His listeners heard a different message in each ear and repeated one of
                        them aloud as they heard it. They could report almost nothing about the
                        other message, not even a switch into German, but usually noticed when
                        its voice changed from male to female.

                        ## The brain picks a winner

                        [Mesgarani & Chang (2012)](https://doi.org/10.1038/nature11020) recorded
                        from the auditory cortex of patients listening to two speakers at once
                        while attending to one. The response tracked the attended speaker so
                        closely that the researchers could reconstruct what that speaker said,
                        as if the other voice were hardly there.

                        ## What helps, and what hurts

                        Listeners separate voices using:

                        - differences in pitch and voice quality,
                        - where each voice comes from,
                        - and knowledge of the language, which fills in what's masked.

                        Hearing loss makes all of this harder, and hearing aids amplify the
                        background along with the voice. Trouble following conversation in a
                        noisy room is often one of the first complaints of people losing their
                        hearing.

                        > Attention doesn't just filter out noise. It reshapes what the auditory
                        > cortex represents.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "music-and-language",
        "created_days_ago": 158,
        "title": "Music and Language",
        "description": "Two sound systems that share more of the brain than you'd expect.",
        "price_cents": 7900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "Shared machinery",
                [
                    lesson(
                        "Two sound systems",
                        """
                        ## More alike than they seem

                        Every known human culture has both language and music. Both:

                        - build large structures from a small set of discrete units, phonemes or
                          notes,
                        - unfold in time, with rhythm and phrasing,
                        - use pitch to carry meaning or emotion,
                        - and are learned early, largely just through exposure.

                        ## And different

                        Language refers: a sentence can tell you where the food is. Music, by
                        and large, doesn't. It conveys emotion and structure, but not
                        propositions. Musical structure is also more flexible: the same melody
                        can be harmonized many ways, while most sentences have only one sensible
                        parse.

                        ## The question

                        Does the brain process them with shared machinery, or separately?
                        Aniruddh Patel, whose book *Music, Language, and the Brain* (2008)
                        frames much of the field, argues the answer is both: separate stores of
                        knowledge, but shared resources for processing structure.

                        This course looks at the evidence on each side: shared brain responses
                        to grammar, disorders that affect one but spare the other, and how music
                        can help language recover after a stroke.

                        > The question isn't whether music is like language, but which parts of
                        > the brain they share.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "Musical syntax in Broca's area",
                        """
                        ## Wrong chords

                        In music, a chord that doesn't fit the key is jarring in much the way a
                        grammatical error is.
                        [Maess et al. (2001)](https://doi.org/10.1038/87502) used MEG to record
                        nonmusicians listening to chord sequences, some of which ended on an
                        unexpected chord.

                        The unexpected chords produced a response called the **early right
                        anterior negativity** (ERAN), which the researchers localized to Broca's
                        area and its counterpart in the right hemisphere.

                        ## The same brain wave

                        Patel and colleagues (1998) found that unexpected chords and
                        grammatically hard sentences both produced a **P600**, a positive brain
                        wave about 600 milliseconds after the event, of similar size and scalp
                        distribution.

                        ## Shared resources

                        Patel's **shared syntactic integration resource hypothesis** proposes
                        that musical and linguistic knowledge are stored separately, but that
                        fitting each new event into a developing structure draws on shared
                        frontal resources.

                        That predicts interference when both are done at once. Studies have
                        found that an unexpected chord makes a syntactically demanding sentence
                        harder to process, while an unexpected change of instrument, surprising
                        but not a violation of musical syntax, doesn't.

                        Not every study agrees. Some imaging work finds that the brain's most
                        language-selective regions barely respond to music, so how much is truly
                        shared remains open.

                        > In the brain, a wrong chord and a wrong word can set off similar
                        > alarms.
                        """,
                    ),
                ],
            ),
            (
                "Where they part",
                [
                    lesson(
                        "Amusia",
                        """
                        ## Tone deafness is real

                        Some people can't tell when a melody is out of tune, can't recognize
                        familiar tunes without their words, and can't tell which of two close
                        notes is higher. This is congenital
                        [amusia](https://en.wikipedia.org/wiki/Amusia), studied in depth by
                        Isabelle Peretz and colleagues in Montreal. Estimates of how many people
                        have it range from about 1.5 to 4 percent.

                        Speech is mostly spared. People with congenital amusia speak and
                        understand normally, and most can hear whether a sentence is a question
                        or a statement. Some have subtle trouble with pitch in speech, when the
                        pitch differences are small.

                        ## Acquired amusia, and the reverse

                        A stroke can cause amusia too, often when the right temporal lobe is
                        involved.

                        The reverse also happens. The Russian composer Vissarion Shebalin had
                        strokes in 1953 and 1959 that left him with severe aphasia. He kept
                        composing, and finished his Fifth Symphony after the second stroke;
                        Dmitri Shostakovich praised it highly.

                        ## What the dissociation shows

                        One person who loses language but keeps music, another who loses music
                        but keeps language: that's a double dissociation. Whatever music and
                        language share, they don't depend on all of the same machinery.

                        > Music and language can come apart, which means they aren't one system.
                        """,
                    ),
                    lesson(
                        "Tone languages and perfect pitch",
                        """
                        ## Pitch that changes meaning

                        In tone languages such as Mandarin, Cantonese, Yoruba and Vietnamese,
                        pitch distinguishes words. In Mandarin, *ma* with a high level tone
                        means "mother"; with a dipping tone, "horse". A large share of the
                        world's languages are tonal.

                        ## Perfect pitch

                        [Absolute pitch](https://en.wikipedia.org/wiki/Absolute_pitch), the
                        ability to name a note without a reference, is rare. A widely quoted
                        estimate for Western populations is fewer than 1 in 10,000 people.

                        Diana Deutsch and colleagues (2006) tested music students at the Central
                        Conservatory of Music in Beijing and at the Eastman School of Music in
                        the United States. Among students who began training at the same age,
                        absolute pitch was far more common in the Mandarin speakers. Deutsch
                        suggested that learning a tone language in infancy tunes the brain to
                        pitch.

                        The groups also differed in other ways, such as genes and teaching
                        methods, and the interpretation is still debated.

                        ## Does music help language?

                        Musicians are often better at hearing pitch differences in an unfamiliar
                        tone language, and some studies find them better at picking speech out
                        of noise. How large the advantage is, and whether music training causes
                        it, are both debated.

                        > In a tone language, getting the pitch wrong changes the word.
                        """,
                    ),
                    lesson(
                        "Reading: singing after stroke",
                        """
                        ## Words that come out in song

                        Clinicians have long noticed that some people with non-fluent aphasia,
                        who struggle to say a short sentence, can sing the words of a familiar
                        song.

                        ## Melodic intonation therapy

                        In 1973 Martin Albert, Robert Sparks and Nancy Helm described
                        [melodic intonation therapy](https://en.wikipedia.org/wiki/Melodic_intonation_therapy).
                        Patients intone short, useful phrases on two pitches while tapping the
                        rhythm with their left hand. The therapist gradually withdraws support,
                        and the phrases move from song toward ordinary speech.

                        ## Why it might work

                        The original idea was that singing recruits right-hemisphere regions
                        left intact when the left hemisphere is damaged. Gottfried Schlaug and
                        colleagues later reported changes in right-hemisphere regions and their
                        connections after intensive therapy.

                        Other researchers argue that the slow, rhythmic delivery matters more
                        than the melody itself, and that singing familiar songs works partly
                        because the words are stored as a single learned unit.

                        ## The evidence

                        Small trials and case series are encouraging, and the therapy is used in
                        clinics worldwide, but large controlled trials are few. Gains are
                        clearest on the practiced phrases, and less clear in everyday
                        conversation.

                        > Singing can't replace speech, but it can sometimes open a way back to
                        > it.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "stuttering-and-fluency",
        "created_days_ago": 144,
        "title": "Stuttering and Fluency",
        "description": "What stuttering reveals about the timing circuits behind fluent speech.",
        "price_cents": 16900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "What stuttering is",
                [
                    lesson(
                        "Repetitions, prolongations and blocks",
                        """
                        ## Three kinds of break

                        [Stuttering](https://en.wikipedia.org/wiki/Stuttering) interrupts the
                        flow of speech in characteristic ways:

                        - **repetitions** of sounds or syllables: "b-b-b-ball",
                        - **prolongations**: "sssssun",
                        - **blocks**, where speech stops altogether with the mouth set for the
                          sound.

                        Many people who stutter also develop secondary behaviors, such as
                        blinking or swapping words, to get through a block or avoid one.

                        ## Who stutters

                        Stuttering usually begins between the ages of 2 and 5. Around 5 percent
                        of children stutter at some point, but most recover, often within a few
                        years, and about 1 percent of adults stutter. Girls are more likely to
                        recover, so among adults who stutter, men outnumber women by around four
                        to one.

                        ## What doesn't cause it

                        Stuttering isn't caused by nervousness, low intelligence or parenting.
                        Anxiety can make it worse, but it's better understood as a consequence
                        of stuttering than a cause.

                        It runs in families, and twin studies point to a large genetic
                        contribution.
                        [Kang et al. (2010)](https://doi.org/10.1056/NEJMoa0902630) linked some
                        cases to mutations in genes such as *GNPTAB*, which help route enzymes
                        to the cell's lysosomes, an unexpected link that is still being worked
                        out.

                        > Stuttering is a disorder of speech timing, not of thought or language.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "The fluency paradox",
                        """
                        ## When stuttering disappears

                        Many people who stutter are fluent, or nearly so, when they:

                        - sing,
                        - speak in unison with someone else, called **choral speech**,
                        - speak in time to a metronome,
                        - or hear their own voice delayed or shifted in pitch.

                        These conditions have something in common. Each gives the speaker an
                        **external** rhythm or cue for when to start the next sound, instead of
                        relying on an internal one.

                        ## Delayed feedback

                        Hearing your own voice through headphones about a fifth of a second late
                        makes most fluent speakers slow down and stumble. Yet in many people who
                        stutter, this delayed auditory feedback improves fluency. Electronic
                        devices based on it have been sold as fluency aids, with mixed results
                        over the long term.

                        ## A clue to the cause

                        If an external beat restores fluency, the problem may lie in the brain's
                        **internal timing**: the signal that says one movement is finished and
                        the next can begin. That points toward the basal ganglia, the subject of
                        the next module.

                        > The same person who stutters can speak fluently, given a different
                        > beat.
                        """,
                    ),
                ],
            ),
            (
                "The circuits",
                [
                    lesson(
                        "Basal ganglia and timing",
                        """
                        ## Internal cues

                        The [basal ganglia](https://en.wikipedia.org/wiki/Basal_ganglia) are a
                        group of structures deep in the brain, including the **caudate nucleus**
                        and **putamen**, that form loops with the cortex through the thalamus.
                        Among other things, they help start learned sequences of movement and
                        signal when one segment ends so the next can begin.

                        Per Alm (2004) proposed that stuttering reflects a weakness in this
                        internal timing signal. External cues, like a metronome, would recruit
                        other routes, through the cerebellum and premotor cortex, which would
                        explain the fluency paradox.

                        ## Evidence

                        Several observations fit:

                        - Parkinson's disease also involves the basal ganglia and makes starting
                          movements hard, and an external rhythm can help people with
                          Parkinson's walk, much as it helps people who stutter talk.
                        - Strokes or injuries affecting the basal ganglia can cause stuttering
                          in adults who never stuttered before. This is **acquired neurogenic
                          stuttering**.
                        - Drugs that boost dopamine can make stuttering worse, and some drugs
                          that block dopamine receptors can reduce it, though with side effects.

                        ## A loop, not a spot

                        Stuttering doesn't come from one damaged area. It looks more like an
                        inefficient circuit linking the basal ganglia, the motor cortex, and the
                        regions that monitor speech as it's produced.

                        > When the internal metronome falters, speech stalls at the start of the
                        > next sound.
                        """,
                    ),
                    lesson(
                        "White matter and the two hemispheres",
                        """
                        ## Wiring under the left motor cortex

                        In 2002 Martin Sommer and colleagues used diffusion imaging in adults
                        who stutter and found weaker white-matter integrity beneath the left
                        **rolandic operculum**, next to the motor areas for the face and larynx.
                        Fibers there link the frontal areas that plan speech with the motor
                        areas that carry it out, and with the auditory regions that check the
                        result.

                        Later studies found related differences in children who stutter, close
                        to the age of onset. That suggests the differences are part of the
                        cause, not just a result of years of stuttering.

                        ## The right hemisphere

                        Imaging studies of adults who stutter often show **more** activity than
                        usual in right-hemisphere regions mirroring the left-hemisphere speech
                        areas.

                        Is that a cause, or an attempt to compensate? Studies of adults who
                        recovered from childhood stuttering suggest recovery depends more on the
                        left hemisphere, which points to compensation.

                        ## Not one cause

                        The brain differences in stuttering are subtle and vary between people.
                        Researchers increasingly see several pathways converging on the same
                        symptom, which may help explain why a given therapy works for some
                        people and not for others.

                        > Stuttering seems to live in the connections more than in any one
                        > region.
                        """,
                    ),
                    lesson(
                        "Reading: therapy that works",
                        """
                        ## For young children

                        Because many children recover on their own, part of the job is deciding
                        when to treat. For preschool children, the best-studied approach is the
                        **Lidcombe Program**, developed in Australia. Parents, trained by a
                        clinician, praise stutter-free speech and occasionally, gently, ask the
                        child to correct a stuttered word, in short daily conversations. A
                        [randomized trial (Jones et al., 2005)](https://doi.org/10.1136/bmj.38520.451840.E0)
                        found it reduced stuttering substantially compared with no treatment.

                        ## For adults

                        Adult therapy usually draws on two approaches, often combined:

                        - **Fluency shaping** teaches a new way of speaking, with slower speech,
                          gentle voice onsets and light contact between the lips and tongue, and
                          practices it until it feels natural.
                        - **Stuttering modification** aims to stutter more easily, with less
                          tension and avoidance, rather than not at all.

                        Relapse is common, so long-term practice matters. No drug is approved
                        for stuttering, though some are being studied.

                        ## Beyond fluency

                        Many adults who stutter care more about saying what they want, when they
                        want, than about sounding fluent. Self-help groups such as the
                        [National Stuttering Association](https://westutter.org/) work to reduce
                        the shame and avoidance that can do more harm than the stutter itself.

                        > Success isn't always speaking without stuttering. Often it's speaking
                        > without avoiding.
                        """,
                    ),
                ],
            ),
        ],
    },
    {
        "slug": "primary-progressive-aphasia",
        "created_days_ago": 130,
        "title": "Primary Progressive Aphasia",
        "description": "Dementias that take language first, and what they reveal about meaning.",
        "price_cents": 19900,
        "status": CourseStatus.PUBLISHED,
        "modules": [
            (
                "A dementia of language",
                [
                    lesson(
                        "Language first",
                        """
                        ## A different kind of dementia

                        Most people link dementia with forgetting. In
                        [primary progressive aphasia](https://en.wikipedia.org/wiki/Primary_progressive_aphasia)
                        (PPA), the first and main problem is language, caused by a
                        neurodegenerative disease, while memory, reasoning and everyday
                        independence are relatively spared at first.

                        The neurologist Marsel Mesulam described the syndrome in 1982, in six
                        patients with slowly worsening aphasia and no wider dementia.

                        ## How it's diagnosed

                        PPA is diagnosed when:

                        - language difficulty is the most prominent problem, from the start and
                          through the first couple of years;
                        - it's the main thing getting in the way of daily life;
                        - and it's caused by a neurodegenerative disease, not a stroke or a
                          tumor.

                        PPA usually begins before 65, often in a person's fifties or sixties.
                        It's one of the frontotemporal dementia syndromes, though some cases are
                        caused by Alzheimer's disease.

                        ## Three variants

                        [Gorno-Tempini et al. (2011)](https://doi.org/10.1212/WNL.0b013e31821103e6)
                        published consensus criteria for three variants, each with its own
                        pattern of symptoms, of atrophy, and of likely underlying disease. This
                        course takes them one at a time.

                        > In PPA, language is the first casualty, and for years it may be the
                        > only one.
                        """,
                        preview=True,
                    ),
                    lesson(
                        "The nonfluent variant",
                        """
                        ## Effortful, ungrammatical speech

                        In the **nonfluent/agrammatic variant**, speaking becomes slow and
                        effortful. Its core features are:

                        - **agrammatism**: short, simplified sentences missing small grammatical
                          words and word endings ("Went store... bought bread");
                        - **apraxia of speech**: trouble planning the movements of speech, with
                          inconsistent sound errors and distortions.

                        At least one is needed for the diagnosis. Understanding single words and
                        knowing what objects are stay largely intact, while understanding
                        grammatically complex sentences often suffers.

                        ## Where and why

                        Atrophy centers on the left posterior frontal lobe and insula, around
                        Broca's area. The usual cause is a frontotemporal lobar degeneration
                        with abnormal **tau** protein, though not always.

                        ## Echoes of Broca

                        The symptoms resemble the non-fluent aphasia that can follow a stroke in
                        the same region, but here they arrive gradually. Over the years, some
                        people lose speech altogether, and some develop movement problems like
                        those of progressive supranuclear palsy or corticobasal syndrome, which
                        are also diseases of tau.

                        > The words are there. Getting them out, in order, is the problem.
                        """,
                    ),
                    lesson(
                        "The logopenic variant",
                        """
                        ## Searching for words

                        *Logopenic* means "few words". In the
                        [logopenic variant](https://en.wikipedia.org/wiki/Logopenic_progressive_aphasia),
                        speech is grammatical and clearly articulated, but slowed by frequent
                        pauses to find words. Its core features are:

                        - trouble retrieving single words, in conversation and when naming
                          things;
                        - trouble **repeating** sentences and phrases, though single words are
                          repeated fine.

                        The repetition problem is thought to reflect a weakness in
                        **phonological short-term memory**, the brief store that holds a
                        sequence of sounds while it's processed. A long sentence overflows it.
                        Speech often has **phonological errors** too, wrong or swapped sounds,
                        as in "tevelision".

                        ## Where and why

                        Atrophy is greatest around the left temporoparietal junction, at the
                        back of the Sylvian fissure. Unlike the other two variants, the usual
                        cause is **Alzheimer's disease**, so it's often described as a
                        language-led form of Alzheimer's. That matters in the clinic: tests for
                        Alzheimer's pathology, such as amyloid PET or spinal fluid tests, can
                        support the diagnosis and open the door to Alzheimer's treatments and
                        trials.

                        ## Easy to miss

                        The logopenic variant was the last of the three to be described, by
                        Gorno-Tempini and colleagues in 2004. Its pauses can pass for ordinary
                        word-finding trouble at first.

                        > Alzheimer's disease doesn't always begin with memory.
                        """,
                    ),
                ],
            ),
            (
                "Losing meaning",
                [
                    lesson(
                        "The semantic variant",
                        """
                        ## Words lose their meanings

                        In the **semantic variant**, also called
                        [semantic dementia](https://en.wikipedia.org/wiki/Semantic_dementia),
                        speech stays fluent and grammatical, but words lose their meaning. The
                        core features are severe trouble naming things and understanding single
                        words. Other common features:

                        - loss of knowledge about the objects themselves, not just their names,
                          especially less familiar ones;
                        - **surface dyslexia**: reading irregular words by the rules, so *pint*
                          rhymes with *mint*;
                        - vague speech, with general words like "thing" standing in for specific
                          ones.

                        Specific knowledge fades first. A person may lose *zebra* and call one a
                        "horse", and later only an "animal".

                        ## Where and why

                        Atrophy is in the **anterior temporal lobes**, usually more on the left.
                        The usual cause is a frontotemporal lobar degeneration with abnormal
                        **TDP-43** protein. When atrophy is mainly on the right, an early sign
                        may be trouble recognizing familiar faces.

                        ## A hub for meaning

                        [Patterson, Nestor & Rogers (2007)](https://doi.org/10.1038/nrn2277)
                        used semantic dementia to argue for a **hub-and-spoke** model of
                        meaning. The features of a concept, such as how a thing looks, sounds
                        and is used, are stored in "spokes" spread across the brain. The
                        anterior temporal lobes act as a **hub** that binds them into one
                        concept. Damage the hub, and knowledge fails in every modality at once.

                        > Semantic dementia shows that meaning has a place in the brain, and
                        > that it can be lost.
                        """,
                    ),
                    lesson(
                        "Reading: therapy and support",
                        """
                        ## No cure yet

                        No treatment yet stops the diseases that cause PPA, though drugs for
                        Alzheimer's disease may be relevant for some people with the logopenic
                        variant. Even so, a lot can help.

                        ## Speech and language therapy

                        Therapy for PPA aims to keep communication going for as long as
                        possible, which means starting early. Approaches include:

                        - **word retrieval training**, practicing the words that matter most to
                          the person, which can help keep them;
                        - **script training**, rehearsing short conversations for situations
                          like ordering at a café or making a phone call;
                        - **communication aids**, such as personal books of photos and key
                          words, or apps, introduced while they can still be learned.

                        Gains tend to be specific to what's practiced, so therapy focuses on the
                        vocabulary and situations that matter in the person's daily life.

                        ## Support for families

                        Because PPA tends to start younger than most dementias, people are often
                        still working, or raising children, when it begins. Communication
                        partner training, which teaches family members to slow down, use yes/no
                        questions and write key words, helps on both sides of the conversation,
                        as it does for aphasia after a stroke.

                        The
                        [Association for Frontotemporal Degeneration](https://www.theaftd.org/)
                        and the [National Aphasia Association](https://aphasia.org/) list
                        support groups and resources.

                        > Therapy can't stop PPA, but it can keep conversations going for
                        > longer.
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
    ("priya.raman@example.com", "reading-and-the-brain", 55),
    ("hannah.becker@example.com", "primary-progressive-aphasia", 48),
    ("tomas.herrera@example.com", "hearing-speech", 35),
    ("daniel.cho@example.com", "how-children-learn-to-talk", 26),
    ("kwame.mensah@example.com", "music-and-language", 20),
    ("aisha.bello@example.com", "reading-and-the-brain", 14),
    ("daniel.cho@example.com", "stuttering-and-fluency", 12),
    ("sofia.lindqvist@example.com", "primary-progressive-aphasia", 9),
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
    ("priya.raman@example.com", "reading-and-the-brain", 5, 53, 34),
    ("hannah.becker@example.com", "primary-progressive-aphasia", 5, 46, 22),
    ("tomas.herrera@example.com", "hearing-speech", 5, 34, 17),
    ("daniel.cho@example.com", "how-children-learn-to-talk", 2, 25, 15),
    ("kwame.mensah@example.com", "music-and-language", 4, 19, 8),
    ("aisha.bello@example.com", "reading-and-the-brain", 2, 13, 7),
    ("daniel.cho@example.com", "stuttering-and-fluency", 1, 11, 11),
    ("sofia.lindqvist@example.com", "primary-progressive-aphasia", 1, 8, 8),
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
    (
        "priya.raman@example.com",
        "reading-and-the-brain",
        5,
        "The dyslexia module finally made sense of what my son's teachers had been telling "
        "us. Clear and well sourced.",
        ReviewStatus.PUBLISHED,
        30,
    ),
    (
        "aisha.bello@example.com",
        "reading-and-the-brain",
        4,
        "Good balance of history and current research. I wanted more on other writing systems.",
        ReviewStatus.PUBLISHED,
        6,
    ),
    (
        "hannah.becker@example.com",
        "primary-progressive-aphasia",
        5,
        "The three variants are explained more clearly here than in anything I read in "
        "training. The therapy lesson is practical, too.",
        ReviewStatus.PUBLISHED,
        20,
    ),
    (
        "tomas.herrera@example.com",
        "hearing-speech",
        3,
        "Solid, but the first module is heavier on ear anatomy than I wanted. The McGurk "
        "lesson is the highlight.",
        ReviewStatus.PUBLISHED,
        15,
    ),
    (
        "kwame.mensah@example.com",
        "music-and-language",
        4,
        "I had no idea perfect pitch might be linked to tone languages. Short and fascinating.",
        ReviewStatus.PUBLISHED,
        7,
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
