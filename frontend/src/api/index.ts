import { apiClient } from "./client";
import {
  ClassifyPayload,
  ClassifyResponse,
  TrainPayload,
  TrainResponse
} from "./types";

export const trainModel = async (payload: TrainPayload) => {
  const { data } = await apiClient.post<TrainResponse>("/train", payload);
  return data;
};

export const classifyReview = async (payload: ClassifyPayload) => {
  const { data } = await apiClient.post<ClassifyResponse>("/classify", payload);
  return data;
};
