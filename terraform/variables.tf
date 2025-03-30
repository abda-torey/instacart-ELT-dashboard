variable "project_id" {
  type        = string
  description = "The project ID for GCP"
}

variable "region" {
  type        = string
  description = "The region where resources will be created"
  default     = "US"
}

variable "bucket_name" {
  type        = string
  description = "The name of the GCS bucket"
}

variable "dataset_id" {
  type        = string
  description = "The BigQuery dataset ID"
}
