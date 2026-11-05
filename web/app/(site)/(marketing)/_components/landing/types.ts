/*
 * Content shapes for the landing page. Anything flagged `placeholder` is
 * invented copy that must be replaced before launch, and shows a dev-only badge.
 */

type Flaggable = { placeholder?: true };

export type HeroContent = {
  eyebrow: string;
  headline: string;
  body: string;
};

export type Stat = Flaggable & {
  value: string;
  label: string;
};

export type Instructor = Flaggable & {
  name: string;
  title: string;
  bio: string[];
  credentials: string[];
};

export type Testimonial = Flaggable & {
  quote: string;
  name: string;
  context: string;
};

export type LandingContent = {
  hero: HeroContent;
  stats: Stat[];
  instructor: Instructor;
  testimonials: [Testimonial, Testimonial, Testimonial];
};
