export type DocType = "news" | "opinion" | "scientific";

export type EntityType = "PER" | "ORG" | "LOC" | "DATE";

export type Entities = {
  PER: string[];
  ORG: string[];
  LOC: string[];
  DATE: string[];
};

export type SearchResult = {
  id: string;
  title: string;
  snippet: string;
  score: number;
  doc_type: DocType;
  entities: Entities;
};
