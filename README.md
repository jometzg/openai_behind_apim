# Azure OpenAI behind APIM Management Sample
This is a sample python console application that calls Azure OpenAI chat completion, but behind Azure APIM Management

## Why would I want to do this?
External applications that need to access Azure OpenAI need to authenticate to Azure OpenAI. For mobile applications, this presents challenges as keys embedded into an application - even if obfuscated, present a security risk.
This repository has a sample python console application which represents a "public" application - an equivalent of a mobile application. It also includes the configuration needed with Azure AD (Entra ID) and API Management to allow this to work in concert.

## Overall Architecture
