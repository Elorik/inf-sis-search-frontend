import type { DocType, Entities } from "./search";

export type NewDocumentPayload = {
  title: string;
  body: string;
  source: string;
  date: string;
};

export type FullDocument = {
  id: string;
  title: string;
  body: string;
  source: string;
  date: string;
  doc_type: DocType;
  entities: Entities;
  tokens: string[];
};
