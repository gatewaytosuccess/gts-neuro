import type { LandingContent } from "../_components/landing/types";

export const landing: LandingContent = {
  hero: {
    eyebrow: "Neurolinguistics",
    headline: "The cognitive science of how language lives in the brain.",
    body: "A self-paced course for curious learners. Create an account to enroll and track your progress across devices.",
  },

  stats: [
    { value: "2,400+", label: "Learners enrolled", placeholder: true },
    { value: "6", label: "Courses in the catalog", placeholder: true },
    { value: "4.8", label: "Average course rating", placeholder: true },
  ],

  instructor: {
    name: "Dr. Elena Marsh",
    title: "Cognitive neuroscientist and lecturer",
    initials: "EM",
    summary:
      "Elena has spent fifteen years studying how the brain turns sound into meaning, first in a clinical aphasia lab and then teaching undergraduate cognitive science.",
    bio: [
      "Elena has spent fifteen years studying how the brain turns sound into meaning, first in a clinical aphasia lab and then teaching undergraduate cognitive science.",
      "Her research followed people relearning words after a stroke, and what those recoveries reveal about how language is organized in a healthy brain.",
      "The courses here follow the same structure as her lectures, written for learners without a science background who want more than a popular-science summary.",
    ],
    credentials: [
      "PhD, Cognitive Neuroscience",
      "Former lecturer in psycholinguistics",
      "Author of 20+ peer-reviewed papers on language processing",
      "Clinical research fellow, aphasia rehabilitation",
    ],
    placeholder: true,
  },

  testimonials: [
    {
      quote:
        "I have been speaking English for forty years and never once wondered how. Three modules in, I can't stop noticing it.",
      name: "Marcus T.",
      context: "Retired engineer",
      placeholder: true,
    },
    {
      quote: "Dense where it needs to be, and never showing off.",
      name: "Priya R.",
      context: "Speech-language graduate student",
      placeholder: true,
    },
    {
      quote:
        "Finally a course that explains the research instead of just the headlines.",
      name: "Jonas W.",
      context: "High school biology teacher",
      placeholder: true,
    },
  ],
};
