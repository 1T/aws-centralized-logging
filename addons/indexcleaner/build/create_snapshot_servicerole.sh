#!/usr/bin/env bash

aws iam create-role --role-name es-s3-repository --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Sid": "", "Effect": "Allow", "Principal": {"Service": "es.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam put-role-policy --role-name es-s3-repository --policy-name es-s3-repository --policy-document file://snapshot_servicerole_policy.json