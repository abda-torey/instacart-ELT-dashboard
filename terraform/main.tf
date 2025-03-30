provider "google" {
  credentials = file("${path.module}/keys/first-key.json")
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id
  project    = var.project_id
  location   = var.region
}
