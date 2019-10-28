
workflow "Build and Deploy" {
  on = "push"
  resolves = [
    "notify on deploy",
  ]
}

action "build image" {
  uses = "actions/docker/cli@76ff57a"
  args = "build -t myproject ."
}

action "tag image gcloud" {
  uses = "actions/docker/tag@76ff57a"
  args = ["myproject", "eu.gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
  env = {
    PROJECT_ID = "myproject-220562"
    APPLICATION_NAME = "myproject"
  }
  needs = ["build image"]
}

action "gcloud auth" {
  uses = "actions/gcloud/auth@8ec8bfa"
  secrets = ["GCLOUD_AUTH"]
}

action "load docker credentials" {
  uses = "actions/gcloud/cli@8ec8bfa"
  args = ["auth", "configure-docker", "--quiet"]
  needs = ["gcloud auth"]
}

action "push to GCR" {
  needs = ["load docker credentials", "tag image gcloud"]
  uses = "actions/gcloud/cli@master"
  runs = "sh -c"
  env = {
    PROJECT_ID = "myproject-220562"
    APPLICATION_NAME = "myproject"
  }
  args = ["docker push eu.gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
}