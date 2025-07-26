output "last_run_md5" {
  description = "MD5 hash of the script at last apply"
  value       = null_resource.delete_default_vpc.triggers["script_md5"]
}
