# Changelog for Annuities FAQ Bot
This is the changelog for the annuities FAQ bot

## [0.0.94] - 2025-08-29
- [CDOCB1-4629] Ann-client content changes

## [0.0.93] - 2025-05-28
- Added 18 new Utterances on the following:
  - FAQAccMaintFPChangeIntent - 1
  - FAQAccMaintLetterForPOAIntent - 1
  - FAQAccMaintWhoAreMyBenesIntent - 1
  - FAQGeneralPhoneNumberIntent - 2
  - FAQOtherOutOfScopeIntent - 4
  - FAQPruHelpContactIntent - 4
  - FAQSIMP_Generic_Intent - 1
  - FAQSIMP_TaxForms_Intent - 1
  - FAQUpdateSystematicWithdrawalIntent - 1
  - FAQValuesAccountValueIntent - 1
  - FAQWhenWillMoneyArriveIntent - 1
  - added "tax forms" value on TaxSlotType
  - added "tax forms" value on "tax forms" key on SimpleSTForGenericIntentSlotType

## [0.0.92] - 2025-03-18
- Verbiage update for Request form for withdrawal
- Updated Subnet Ids

## [0.0.91] - 2025-02-07
- Verbiage update for Tax forms

## [0.0.90] - 2025-01-06
- Verbiage change for RMD - FAQAboutRMDIntent
- Updated Line 27 of manifest file to fix deployment issue. From /co/aws-infra to /gt/ce/artifactory

## [0.0.89] - 2024-12-16
- Change BotCFN version

## [0.0.88] - 2024-11-20
- Fix 14 missed utterances and 3 Utterances for ProcessCustDupTaxFormIntent
- Updated Runtime from python3.8 to python3.9
- Updated S3 Buckets configuration. Removed bucket for audio logs.
- Verbiage update for FAQInqTaxFormsImportTaxSoftwareIntent

## [0.0.87] - 2024-05-22
- Lead Feedback - Add prefix static value at single place and update test_util code.Update test shell file for enviroment check

## [0.0.86] - 2024-05-16
- Implementation - Client Feedback: Prefix added to symmetrically encryted fields
- Test case - symmetric encryption payload updated along with decryption logic incorporating prefix added

## [0.0.85] - 2024-05-15
- Implementation - Encryption logging code modified to create single symmetric key for request and response turn and updated encryption logic for list data field of response event
- Test case - Session timeout prompt updated

## [0.0.84] - 2024-05-01
- Verbiage update for lex timeout message.

## [0.0.83] - 2024-04-23
- Verbiage and main menu suggestion chip update for tech issue and unsupported intent scenario.
- Test case updated for above scenarios.

## [0.0.82] - 2024-04-18
- Updated the failed test cases and created a new test case for custom timeout message in case of lex session time out.

## [0.0.81] - 2024-04-12
- Implemented Lead Feedback, made asymmetric and hybrid encryption decryption configurable, resolved merge conflicts in Changelog file, corrected the date format in the previous commit and updated the encryption test case.

## [0.0.80] - 2024-04-11
- Bug fixed - Timeout Fallback message is displayed instead of second fallback message, it contains code changes

## [0.0.79] - 2024-04-09
- Added test case for Hybrid Encryption Decryption.

## [0.0.78] - 2024-04-08
- Implemented efficient encryption using Hybrid Approach (Asymmetric + symmetric).

## [0.0.77] - 2024-03-26
- code change - fixed stage defect: bot was not taking feedback description was triggering fallback intent, added condition check in fallback intent.

## [0.0.76] - 2024-03-26
- Resolved merge conflicts

## [0.0.75] - 2024-03-25
- code change - Fast follow item in code refactor branch, new logic to validate the contract number, must to have mini 3 digits, hyper link add for phone number in verbiage, custom message when there are no options to show

## [0.0.74] - 2024-03-20
- code change - Fast follow item, new logic to validate the contract number, must to have mini 3 digits

## [0.0.73] - 2024-03-06
- code change - verbiage update to add the hyperlink to the phone number

## [0.0.72] - 2024-02-23
- code change - Lead feedback implemented, fast follow item to updated the suggestion chip when there are no suggestions to show

## [0.0.71] - 2024-02-15
- code change - Adding a custom fallback message for the session timeout scenario

## [0.0.70] - 2024-02-14
- code change - Fast foloow item fix- adding context for casual talk, to show cusotm fallback message if there are no options to show.

## [0.0.69] - 2024-01-17
- Code Change - Empty list check added for Reprint API response

## [0.0.68] - 2024-01-09
- Code Change - Reprint api response handling updated

## [0.0.67] - 2024-01-04
- Code Change - Document mail Success response updated with form details

## [0.0.66] - 2024-01-04
- Code Change - Document mail Success response updated

## [0.0.65] - 2023-12-29
- Code Change - content changes updated for FAQAboutRMDIntent

## [0.0.64] - 2023-12-27
- Code Change - FAQ response updated for FAQAboutRMDIntent

## [0.0.63] - 2023-12-13
- Code Change - FAQ response updated with tax form button and hr tag modified in json file and styling updated in temporary code change
- Bot Change - New utterances were added to tax form flow and bot tunned

## [0.0.62] - 2023-12-12
- Updated HR Line Break between paragraph

## [0.0.61] - 2023-12-11
- Code Update : Sagemaker API call exception handled and timeout parameter set to 60 seconds

## [0.0.60] - 2023-12-11
- Code Update : Encrypting lambda logs for all intents, as session attributes holds Utterance history

## [0.0.59] - 2023-12-07
- Verbiage update: Fallback message for invalid contract number updated

## [0.0.58] - 2023-12-06
- Change: Bug fixes and output context added in bot intent "are you a chatbot"

## [0.0.57] - 2023-12-06
- Bot change: Bot tunned with new utterances

## [0.0.56] - 2023-12-05
- Code change: Tax form flow verbiage updated

## [0.0.55] - 2023-12-04
- Code change: [CDOCB1-3063] Remove Utterances from printing in the logs

## [0.0.54] - 2023-12-01
- Code change: Slot prompt counter loop issue resolved

## [0.0.53] - 2023-11-30
- Code change: [CDOCB1-3132] One source document search, no tax form response handling updated

## [0.0.52] - 2023-11-02
- Code change: [CDOCB1-2914] Missing request attributes added in response
- Bot change: Request online utterance added in bot faq intent

## [0.0.51] - 2023-10-25
- Integrated Data Science Model when Bot encounters fallback and printing them in logs
- Moved Environment specific creds to individual files in config/{dev,qa,stage,prod}.yaml locations
- Optimized Session Attributes Logic

## [0.0.50] - 2023-09-13
- Updated Bitly link for FAQOtherOutOfScopeIntent in data.csv [CDOCB1-2757]

## [0.0.49] - 2023-09-12
- Updated Bitly link for FAQOtherOutOfScopeIntent in data.csv [CDOCB1-2757]

## [0.0.48] - 2023-09-08
- Updated content change for FAQPruHelpRetrieveUserIDIntent in data.csv [CDOCB1-2757]

## [0.0.47] - 2023-09-07
- Updated bitly links in data.csv and config.json [CDOCB1-2757]

## [0.0.46] - 2023-07-05
- Implement Adavance tuning changes in bot [CDOCB1-2536]

## [0.0.45] - 2023-05-16
- Change logging level to "info"; debug will debug secretsmanager data

## [0.0.44] - 2023-05-16
- Minor: Reset to enable lex audio logs (undo part of 0.0.43)

## [0.0.43] - 2023-05-16
- Proper syntax for encrypting all contextAttributes under log and disable lex audio logs

## [0.0.42] - 2023-05-16
- Addressing encryption of contextAttributes and disabling of lex text logs

## [0.0.41] - 2023-05-05
- Updating the encryption logger key name

## [0.0.40] - 2023-04-19
- Handle response from proxy for duplicate tax form [CDOCB1-2286]

## [0.0.39] - 2023-04-12
- The welcome message format changed, desc of bot updated [CDOCB1-1980]

## [0.0.38] - 2023-04-12
- The welcome message is added to config.json and printed through code [CDOCB1-1980]

## [0.0.37] - 2023-04-07
- Content change - Updated the welcome message [CDOCB1-1980]

## [0.0.37] - 2023-04-07
- Content change - Updated the welcome message [CDOCB1-1980]

## [0.0.36] - 2023-03-03
- Updated lambda for client use case
- Added layer for cryptography
- Added Secret manager for keys
- Added HandleProxyReqResponseIntent for handling client bot proxy api response

## [0.0.35] - 2023-02-24
- Content change - Updated the response in FAQOtherOutOfScopeIntent with Main Menu Suggestion in data.csv file [CDOCB1-1908]

## [0.0.34] - 2023-02-24
We are fine tuning the bot with given files shared by business,
- 20 Failing out of 56 Utterances from 02/17 [CDOCB1-1908]
- For 20 Utternces which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4937) passed in the Main input file.
- Content change - Updated the responses in FAQAccMaintOptForPaperlessIntent, FAQOtherOutOfScopeIntent in data.csv file.

## [0.0.33] - 2023-02-09
We are fine tuning the bot with given files shared by business,
- 19 Failing out of 54 Utterances from 02/01 [CDOCB1-1831]
- For 19 Utternces which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4884) passed in the Main input file.

## [0.0.32] - 2023-02-07
- Added Process Cust duplicate tax form intent for handling client bot scenario
- [CDOCB1-1608] Masking of Personal Data in Chatbot

## [0.0.31] - 2023-01-25
We are fine tuning the bot with given files shared by business,
- 16 Failing out of 45 Utterances from 01/20 [CDOCB1-1723]
- For 16 Utternces which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4842) passed in the Main input file.

## [0.0.30] - 2023-01-12
We are fine tuning the bot with given files shared by business,
- 5 Failing out of 19 Utterances from 01/06 [CDOCB1-1628]
- For 5 Utternce which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4825) passed in the Main input file.

## [0.0.29] - 2023-01-12
- deploying the previous sprint bot zip file.

## [0.0.28] - 2023-01-11
- updated the bot zip file.

## [0.0.27] - 2023-01-11
We are fine tuning the bot with given files shared by business,
- 5 Failing out of 19 Utterances from 01/06 [CDOCB1-1628]
- For 5 Utternce which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4825) passed in the Main input file.
- Content change - Updated the tax responses in FAQAccMaintViewDocsOnlineIntent, FAQSIMP_Generic_tax forms intent in data.csv file.

## [0.0.26] - 2022-12-23
We are fine tuning the bot with given files shared by business,
- 1 Failing out of 5 Utterances from 12/14 [CDOCB1-1622]
- For 1 Utternce which is failed were unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4820) passed in the Main input file.

## [0.0.25] - 2022-12-14
- Updated the correct url for [ online ] in the response for the FAQNewBusinessOpenContractIntent [CDOCB1-1384]

## [0.0.24] - 2022-12-13
- Updated the correct url for [financial professional] in the response for the FAQNewBusinessOpenContractIntent

## [0.0.23] - 2022-12-13
- Bot Tuning - 3 Failing out of 13 Utterances from 12/9 [CDOCB1-1448]
- For 3 Utternces which is failed were due to long utterance and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4753) passed in the Main input file.
- Content Changes - Created 6 new intents and their respective Utterances in the bot [CDOCB1-1384]
- Added the responses for the newly created intent in data.csv file.
- Updated the 3 responses for the existing intents in data.csv file.

## [0.0.22] - 2022-12-01
We are fine tuning the bot with given files shared by business,
- 2 Failing out of 5 Utterances from 11/28 [CDOCB1-1390]
- For 2 Utternces which is failed were due to long utterances, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4748) passed in the Main input file.

## [0.0.21] - 2022-11-16
We are fine tuning the bot with given files shared by business,
- 2 Failing out of 12 Utterances from 11/11 [CDOCB1-1377]
- For 2 Utternces which is failed were due to long utterances, we have added the phrases/keywords that is already present in the respective intents
- All Utterances(4736) passed in the Main input file.

## [0.0.20] - 2022-11-10
- renamed the resources_yaml.txt.yaml file to resources_yaml.txt

## [0.0.19] - 2022-11-07
We are fine tuning the bot with given files shared by business,
- 13 Failing out of 47 from 11/01 [CDOCB1-1345]
- For 13 Utternces which is failed were due to long utterances and unable to fix, we have added the phrases/keywords that is already present in the respective intents
- 1 failing in Main Input File Utterances(4689) and that utterance is manually passed in Bot.

## [0.0.18] - 2022-10-10
We are fine tuning the bot with given files shared by business,
- 12 Failing out of 26 from 9/27 [CDOCB1-1245]
- All Utterances(4663) passed in the Main input file.

## [0.0.17] - 2022-09-28
- Changed the current star feedback rating system to a "Yes - My question got answered" and "No - My question did not get answered, For No, We are collecting feedback  comments from customer and storing in the logs
- Added "Go back to the Main Menu" after the user would enter a feedback response.

## [0.0.16] - 2022-09-07
We are fine tuning the bot with given files shared by business, since to decrease fallbacks in prod ASAP, we are sending the current bot in a phase manner.
- Merged both 437 and 170 files into Main input file and got new list of 64 utterances received on 8/24
- From last build, we fixed this utterance "How do I return forms , return forms" in the bot, the count of 74 and 64 file incresed by 2 , but those were the long utterance we have added the phrases/keywords that is already present in the respective intents.
- 10 Failing out of 74 from 8/18 [CDOCB1-1135]
- 7 Failing out of 64 from 8/24 [CDOCB1-1143]
- 10 Failing out of 4681 from Main Input File

## [0.0.15] - 2022-09-06
We are fine tuning the bot with given files shared by business, since to decrease fallbacks in prod ASAP, we are sending the current bot in a phase manner.
- Merged both 437 and 170 files into Main input file and got new list of 64 utterances received on 8/24
- 8 Failing out of 74 from 8/18 [CDOCB1-1135]
- 5 Failing out of 64 from 8/24 [CDOCB1-1143]
- 10 Failing out of 4681 from Main Input File

## [0.0.14] - 2022-08-26
 - [CDOCB1-829] Promoting Online Registration/Self Service within the Welcome Message
 - Feedback Message Update

## [0.0.13] - 2022-08-24
We are fine tuning the bot with given files shared by business, since to decrease fallbacks in prod ASAP, we are sending the current bot in a phase manner.
- Merged both 437 and 170 files and got new list of 69 utterances received on 8/18
- 25 Failing out of 437 from 6/16 and 170 from 7/21 [CDOCB1-736], [CDOCB1-825], [CDOCB1-793]
- 12 Failing out of 69 from 8/18 [CDOCB1-1135]
- 03 Failing out of 4000 from Main Input File [CDOCB1-798]

## [0.0.12] - 2022-08-08
We are fine tuning the bot with given files shared by business, since to decrease fallbacks in prod ASAP, we are sending the current bot in a phase manner.
- 36 Failing out of 437 from 6/16
- 19 Failing out of 170 from 7/21
- 10 Failing out of 4000 from Main Input File

## [0.0.11] - 2022-08-05
- Long Utterance Reaction [CDOCB1-768]
- Fixed cfnlint error on S3 bucket policy(securetransport)

## [0.0.10] - 2022-08-01
We are fine tuning the bot with given files shared by business, since to decrease fallbacks in prod ASAP, we are sending the current bot in a phase manner.
- 50 Failing out of 437 from 6/16
- 24 Failing out of 170 from 7/21
- 31 Failing out of 4000 from Main Input File

## [0.0.9] - 2022-06-29
- Introducing hyperlink for self servicing suggestion [CDOCB1-728]
- Added Paragraph break in bot responses [CBOCB1-580]

## [0.0.8] - 2022-06-24
- Added 14 new intents and 2 content changes [CBOCB1-600]
- Fixed 25 Failed utterances - [CBOCB1-745] [CBOCB1-746]
- New verbiage for welcome message

## [0.0.7] - 2022-06-20
- Added 19 new intents
- Updated content to questions to improve recognition
- Corrected errors in utterances
- New release CDOCB1-335

## [0.0.6] - 2022-03-16
- Move FAQs from Kendra to Lex
- Move FAQ data into Lambda's data.csv file

## [0.0.6] - 2022-01-07
- Add extra RSM and update data classification to Public
- Content update for messages (e.g., I'm ready to move on)
  and line spacing, based on business testing feedback
- Minor change in text message for suggestion chips
- Minor change in src/config.json (messages updated)

## [0.0.5] - 2022-01-06
- Improved docstrings to relevant methods with parameters
- Text content extensively tested by business

## [0.0.4] - 2022-01-04
- Moved standard message payloads into config.json
- Minor content changes based on user testing feedback
- Fix runtime and handler in lambda template
- Updates to FAQ templates (format and answers) based on
  business testing feedback
 
## [0.0.4] - 2022-01-04
- Updates to retention times and IAM roles
- Minor intent changes in Lex

## [0.0.3] - 2021-12-22
- Kendra.yaml has new FAQ sections and one additional facet
- Updates to faq_templates folder (new FAQ sections and content)
- Changes to lambda function to reflect updated format

## [0.0.2] - 2021-12-14
- Update Jenkinsfile to correct repo and branch
 
## [0.0.1] - 2021-12-09
- Initial Commit
