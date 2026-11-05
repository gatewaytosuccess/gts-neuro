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
    bio: [
      "Elena has spent fifteen years studying how the brain turns sound into meaning, first in a clinical aphasia lab and then teaching undergraduate cognitive science.",
      "She built this course for the people who kept stopping her after public lectures to ask one more question.",
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

  buying: {
    eyebrow: "Buying a course",
    title: "One payment, and the course is yours.",
    items: [
      {
        title: "Keep it for good",
        body: "Pay once and keep lifetime access to every lesson.",
      },
      {
        title: "Try before you buy",
        body: "Most courses have free preview lessons, and you can open them without an account.",
      },
    ],
    cta: { label: "Browse courses", href: "/courses" },
  },
};
