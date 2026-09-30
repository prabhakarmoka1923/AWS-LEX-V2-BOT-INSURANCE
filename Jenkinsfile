#!/usr/bin/env groovy
     properties([
          parameters([
    string(name: 'bb_url', defaultValue: "[[sourceType: 'GitSCM', url: 'hhttps://pramerica-bitbucket.prudential.com/scm/ceac/cdo_gtcdoconvp.git' , branchName: 'feature/cdo-lex-annuities-faq', nodeName:'linux', stageName: 'Load config', bbCredId:'BitbucketPRD']]")
  ])
])
library "SDPLibrary@master"
basePipeline(); 
