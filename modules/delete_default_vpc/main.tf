data "local_file" "script" {
  filename = var.script_path
}

resource "null_resource" "delete_default_vpc" {
  triggers = {
    script_md5 = data.local_file.script.content_md5
  }

  provisioner "local-exec" {
    command     = "python3 ${var.script_path}"
    interpreter = ["bash", "-c"]
  }
}
