## site.pp ##

## Active Configurations ##

# Disable filebucket by default for all File resources:
File { backup => false }

# DEFAULT NODE

node default {
  class { 'apache':
  #  default_vhost => false
  }
  # set up proxy server
  class { 'apache::mod::proxy': }
}
