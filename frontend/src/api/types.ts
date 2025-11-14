export interface TrainPayload {
  fresh_samples: string[];
  rotten_samples: string[];
  use_default_dataset: boolean;
  alpha: number;
}

export interface TrainResponse {
  message: string;
  fresh_token_count: number;
  rotten_token_count: number;
  vocabulary_size: number;
  top_fresh_words: string[];
  top_rotten_words: string[];
}

export interface ClassifyPayload {
  review: string;
}

export interface ClassifyResponse {
  label: string;
  fresh_probability: number;
  rotten_probability: number;
  tokens_considered: string[];
}
