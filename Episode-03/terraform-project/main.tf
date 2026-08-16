# ============================================
# Creates: GCP VPC + Public Subnet + VM
# State: Stored in GCS bucket
# ============================================

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # GCS bucket must already exist
  backend "gcs" {
    bucket = "mysecondbucketterra"
    prefix = "terra/harness-demo1"
}
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
  zone    = var.gcp_zone
}

variable "gcp_project" {
  description = "GCP project ID"
  type        = string
}

variable "gcp_region" {
  default = "us-central1"
}

variable "gcp_zone" {
  default = "us-central1-a"
}

# ============================================
# VPC
# ============================================

resource "google_compute_network" "demo" {
  name                    = "harness-demo-vpc"
  auto_create_subnetworks = false
}

# ============================================
# Public Subnet
# ============================================

resource "google_compute_subnetwork" "demo" {
  name          = "harness-demo-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.gcp_region
  network       = google_compute_network.demo.id
}

# ============================================
# Firewall - Allow HTTP/HTTPS
# ============================================

resource "google_compute_firewall" "demo" {
  name    = "harness-demo-firewall"
  network = google_compute_network.demo.name

  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["harness-demo"]
}

# ============================================
# Firewall - SSH
# ============================================

resource "google_compute_firewall" "ssh" {
  name    = "harness-demo-ssh"
  network = google_compute_network.demo.name

  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["harness-demo"]
}

# ============================================
# Compute Engine VM
# ============================================

resource "google_compute_instance" "demo" {
  name         = "harness-demo-vm"
  machine_type = "e2-micro"
  zone         = var.gcp_zone

  tags = ["harness-demo"]

  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/family/debian-12"
      size  = 10
      type  = "pd-standard"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.demo.id

    # Ephemeral public IP
    access_config {}
  }

  labels = {
    name = "harness-demo-vm"
  }
}

# ============================================
# Outputs
# ============================================

output "vpc_id" {
  value = google_compute_network.demo.id
}

output "subnet_id" {
  value = google_compute_subnetwork.demo.id
}

output "vm_public_ip" {
  value = google_compute_instance.demo.network_interface[0].access_config[0].nat_ip
}

output "vm_instance_id" {
  value = google_compute_instance.demo.id
}
