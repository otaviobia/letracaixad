export enum RatingEnum {
  ABISMO = 1,
  NAO_E_PRA_MIM = 2,
  ESQUECIVEL = 3,
  MANEIRO = 4,
  PEAK_FICTION = 5,
}

// A interface do Review que vem da API
export interface Review {
  id: number;
  title: string;
  content_type: string; // "filme", "jogo", etc
  cover_image_url: string;
  reaction_gif_url?: string; // Opcional
  review_markdown: string;   // O texto completo
  rating: RatingEnum;
  tags_list: string;
  external_link?: string;
  time_spent?: string;
  created_at: string; // Vem como string ISO do backend
}