#!/bin/bash

cd "../.."
bundle exec jekyll serve -I --config _config.yml,_config.dev.yml
cd ./scripts/linux/