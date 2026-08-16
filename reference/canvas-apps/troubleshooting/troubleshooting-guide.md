# Power Apps troubleshooting — extracted text

> Extracted from `troubleshoot-power-platform-power-apps.pdf` (Microsoft Learn, 296 pages, 21.7 MB) with `pdftotext -layout`. Companion to the curated `official-docs/` extractions of `power-apps-maker.pdf`. Page breaks appear as `---`.

## Contents

- [Power Apps troubleshooting strategies](#power-apps-troubleshooting-strategies)
- [Troubleshoot broken connections](#troubleshoot-broken-connections)
- [Troubleshoot Power Apps flow integration](#troubleshoot-power-apps-flow-integration)
- [Troubleshoot HTTP 0 responses and other blocked calls](#troubleshoot-http-0-responses-and-other-blocked-calls)
- [Troubleshoot Power Query issues](#troubleshoot-power-query-issues)
- [Common issues and resolutions for Power Apps](#common-issues-and-resolutions-for-power-apps)
- [Debug canvas apps by using Live monitor](#debug-canvas-apps-by-using-live-monitor)
- [Debug canvas apps without Live monitor](#debug-canvas-apps-without-live-monitor)
- [How to create a minimal repro canvas app](#how-to-create-a-minimal-repro-canvas-app)
- [Isolate issues in canvas apps](#isolate-issues-in-canvas-apps)
- [Troubleshoot date and time issues in Power Apps canvas apps](#troubleshoot-date-and-time-issues-in-power-apps-canvas-apps)
- [Troubleshoot common issues when using](#troubleshoot-common-issues-when-using)
- [Azure key vault errors in wrap for Power](#azure-key-vault-errors-in-wrap-for-power)
- [How to create a vanilla repro model-driven app](#how-to-create-a-vanilla-repro-model-driven-app)
- [Isolate issues in model-driven apps](#isolate-issues-in-model-driven-apps)
- [Troubleshoot date and time issues in model-driven apps](#troubleshoot-date-and-time-issues-in-model-driven-apps)
- [Troubleshoot Lookup control issues in](#troubleshoot-lookup-control-issues-in)
- [Troubleshoot view issues in model](#troubleshoot-view-issues-in-model)
- [Troubleshooting grid issues in Power](#troubleshooting-grid-issues-in-power)
- [Troubleshooting ribbon issues in Power](#troubleshooting-ribbon-issues-in-power)
- [Troubleshooting Word templates](#troubleshooting-word-templates)
- [Known issues with document](#known-issues-with-document)
- [Troubleshooting server-based](#troubleshooting-server-based)
- [Troubleshooting conditional access](#troubleshooting-conditional-access)
- [Troubleshoot SharePoint integration](#troubleshoot-sharepoint-integration)
- [Troubleshooting document](#troubleshooting-document)
- [Troubleshoot offline sync errors in the](#troubleshoot-offline-sync-errors-in-the)
- [Troubleshooting startup or sign-in issues](#troubleshooting-startup-or-sign-in-issues)

---


## Power Apps troubleshooting strategies

Power Apps troubleshooting
Welcome to Power Apps troubleshooting. These articles explain how to determine, diagnose,
and fix issues that you might encounter when you use Power Apps. In the navigation pane on
the left, browse through the article list or use the search box to find issues and solutions.



  Canvas apps


  ｃ HOW-TO GUIDE
  Common issues and resolutions for Power Apps

  Isolate issues in canvas apps

  How to create a minimal repro canvas app

  Troubleshoot date and time issues in Power Apps canvas apps

  Troubleshoot canvas app performance issues

  Troubleshoot startup issues for Power Apps

  Troubleshoot Power Query issues




  Model-driven apps


  ｃ HOW-TO GUIDE
  Isolate issues in model-driven app

  How to create a vanilla repro model-driven app

  Troubleshoot date and time issues in model-driven apps

  Troubleshoot Lookup issues in model-driven apps

  Troubleshoot view issues in model-driven apps

  Troubleshoot grid issues in model-driven apps




  Connections

  ｃ HOW-TO GUIDE
---


## Troubleshoot broken connections

Troubleshoot broken connections

Connection errors when running flows in Power Apps

Troubleshoot HTTP 0 responses and other blocked calls




Documentation and training


ｉ REFERENCE
Power Apps documentation

Power Apps training




Support Resources


ｉ REFERENCE
Power Apps support

Power Apps Community forum

Power Apps Ideas forum
---

Troubleshoot Power Apps canvas app
performance issues
Article • 02/14/2025



   Tip

  For performance issues, you can use profiling tools like Monitor and Performance
  insights to debug and diagnose problems.


The following table outlines common performance issues you might encounter while
using a canvas app, along with likely causes and recommendations. High-level issues are
linked to more detailed documentation through their associated causes and
recommendations. Some recommendations might appear multiple times, as the root
cause can manifest in various symptoms.


                                                                                  ﾉ     Expand table


 Problem/Symptom            Likely cause               Recommendations

 Slow app/page load times   - Overloaded OnStart       - Move calculations out of OnStart
                            - Large data sets          - Use small data payloads
                            - Many cross-screen        - Defer loading data
                            references                 - Optimize resource usage – media,
                            - Heavy media files        controls, references

 Large data payloads        - Retrieving unnecessary   - Use small data payloads
                            data                       - Use delegation
                            - Large data sets          - Prefilter data at the source
                                                       - Limit data retrieval

 Inefficient data queries   - Nondelegable queries     - Use delegation
                            - Complex data             - Optimize query patterns
                            operations

 Inefficient calculations   - Complex formulas         - Optimize formulas
                            - Repeated calculations    - Split up long formulas

 Overall slow app           - Inefficient data         - Optimize data sources
 performance                retrieval                  - Optimize formulas
                            - Many cross-screen        - Use collections for small, frequently
                            references                 used data
                            - Complex formulas         - Split up apps
                            - Overly large apps
---

More information
For an overview of how to create a performant canvas app, see the Overview of creating
performant apps.

For more information and guidance on creating performant apps, see:

     Small data payloads - limit the amount of data you get
     Optimized data query patterns
     Optimize app or page load for peak performance
     Fast calculations

For more information on debugging canvas apps and performance issues, see:

     Understand canvas app execution phases and performance monitoring
     Creating performant apps
     Common canvas app performance issues and resolutions
     Debugging canvas apps with Monitor

For functionality or performance issues with model-driven apps, see Power Apps
troubleshooting strategies.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Refresh URL isn't displayed for custom
connectors when using Generic Oauth 2
Article • 11/30/2022


Applies to: Power Platform, Custom Connectors



Symptoms
When you try to verify the configuration of custom connectors that use Generic Oauth 2
as the identity provider, you experience the following issues:

      The Security page shows placeholder text instead of the configured value in the
      Refresh URL field.




      In the Swagger Editor, the Refresh URL value isn't listed or displayed as a security
      definition.




Cause
These issues are by design. After a custom connector is created, the configured Refresh
URL value isn't displayed on either the Security page or in the Swagger Editor even
though the other fields are populated as expected.



Workaround
To update the Refresh URL value of a custom connector, you can set the value on the
Security page, and select Update connector. Then, the value will be updated and saved
to the connector configuration even though the configured value isn't displayed. For
more information, see the OAuth 2.0 authentication type.
---

Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

Troubleshoot broken connections in
Microsoft Power Platform

Summary
Connections in Microsoft Power Platform can break for several reasons. These causes include
expired tokens, Data Loss Prevention (DLP) blocks, password changes, Conditional Access
policy mismatches, and disabled accounts. This article helps you identify the cause and fix
broken connections in Power Automate.

     Connection times out
     DLP block occurs
     Invalid authenticated devices are used
     Inactivity persists for a long time
     Connection problem related to attended mode occurs
     Password modification is made by a user
     Microsoft Entra ID configuration is changed
     Connection owner account is deleted or disabled
     Tenant administrator disables the application
     Conditional Access policy mismatch for embedded flows occurs
     Terms of Use policy breaks flow connections


Connection times out
This problem occurs if a client (such as a web browser or an application) tries to establish a
connection to a server, but the server doesn't respond within a specified time limit. Several
conditions can cause this problem, such as the server being offline, network issues, or the
server taking too long to process the request. When the connection times out, the client stops
waiting for a response, and terminates the connection attempt.

You might also receive the following error message:

  The user could not be authenticated as the grant is expired. The user must sign in again.



Solution
---

   1. Check your internet connection: Make sure that the internet connection is stable and
     working correctly.
   2. Check the server status: Verify that the server you're trying to connect to is online and not
     experiencing any downtime.
   3. Try increasing the timeout limit: Sometimes, increasing the timeout limit can help
     establish a connection to the server.


DLP block occurs
Data Loss Prevention (DLP) is a security measure that prevents sensitive information from being
shared or transferred inappropriately. A DLP block occurs if a DLP policy detects that an action,
such as sending an email message or sharing a file, violates the organization's data protection
rules. The DLP system then blocks the action to prevent potential data breaches or
unauthorized access to sensitive information.

When a DLP block occurs, you might also receive one of the following error messages:

        Access has been blocked by Conditional Access policies. The access policy does not
        allow token issuance.
        Device is not in required device state: domain_joined. Conditional Access policy
        requires a domain joined device, and the device is not domain joined.



Solution
   1. Review DLP policies: Check the DLP policies configured in the organization to understand
     what actions are blocked and why.
   2. Consult with your administrator: If they blocked the connector or connection, request that
     they unblock it.


Invalid authenticated devices are used
This situation occurs if a user tries to authenticate by using a device for multifactor
authentication (MFA), but the device is disabled. This problem isn't related to Power Automate
but to the tenant's configuration at the administrative level.

In this situation, you might also receive one of the following error messages:

        Device object was not found in the tenant '<TenantID>' directory.
---

        Device is not in required device state: compliant. Conditional Access policy requires a
        compliant device, and the device is not compliant. The user must enroll their device
        with an approved MDM provider like Intune.
        Device used during the authentication is disabled.
        Application needs to enforce Intune protection policies.
        Error from token exchange. Permission denied due to missing connection ACL.



Solution
   1. Contact the tenant administrator to understand why the device was disabled.
   2. Try to reauthorize the connection.


Inactivity persists for a long time
This situation occurs if a connection becomes invalid because it isn't used for a specified
period. For example, the SharePoint connector requires usage at least one time every 90 days
to remain active. If you don't use the connection within this period, the connection expires.

For more information, see Refresh tokens in the Microsoft identity platform.

In this situation, you might also receive one of the following error messages:


        The refresh token has expired due to inactivity. The token was issued on <DateTime>
        and was inactive for 90.00:00:00.
        The provided authorization code or refresh token has expired due to inactivity. Send a
        new interactive authorization request for this user and resource.



Solution
Create a new connection or reauthorize the existing one.


Connection problem related to attended mode
occurs
This situation refers to problems that occur if a user tries to use features that require a license
for unattended mode but the user doesn't have the necessary license. In attended mode, the
user must be present and interact with the system. However, unattended mode provides fully
---

automated processes without user interaction. If a user without the appropriate license tries to
use unattended mode, the connection fails.

Learn more about attended and unattended scenarios for process automation.


Solution
Make sure that the user has the correct license to interact with the system as required in
unattended mode. For more information, see Which Power Automate licenses do I need?


Password modification is made by a user
This problem occurs if you delete or change a password for the account that you use to create
the connection, or you let the password expire. Because account verification is a crucial part of
authentication whenever you trigger a connection, the connection breaks if you don't update
the new password.

You might also receive the following error message:


  The provided grant has expired due to it being revoked, a fresh auth token is needed. The
  user might have changed or reset their password. The grant was issued on '<DateTime>'
  and the TokensValidFrom date (before which tokens are not valid) for this user is
  '<DateTime>'.



Solution
Every time that you update your password, you invalidate the existing connection that uses the
old password. You must create a connection for each of those connectors, or edit the existing
connection. To avoid this problem, use services such as Microsoft Entra ID.


Microsoft Entra ID configuration is changed
This problem refers to modifications that are made at the Microsoft Entra ID (formerly Azure
Active Directory) level that affect user identities or access policies. These changes include
moving to a new location, altering user roles, and updating security settings. Such changes
might invalidate existing tokens and require users to reauthenticate.

You might also receive the following error message:
---

  Due to a configuration change made by your administrator, or because you moved to a
  new location, you must use multi-factor authentication to access '00000003-0000-0000-
  c000-000000000000'.



Solution
Contact the tenant administrator to understand the specific changes and reauthorize the
connection, if necessary.


Connection owner account is deleted or disabled
This situation occurs if the account that created a connection is removed or disabled in the
directory. In this situation, the connection becomes invalid and affects all users who share it.

You might also receive one of the following error messages:


       The user account {EUII Hidden} has been deleted from the <DirectoryID> directory.
       To sign into this application, the account must be added to the directory.
       The user account is disabled.
       The user account {EUII Hidden} does not exist in the <DirectoryID> directory. To sign
       into this application, the account must be added to the directory.



Solution
To resolve this problem, have another user who has access reauthorize the connection. This
action updates the ownership and restores functionalities for all users.


Tenant administrator disables the application
This situation occurs if the tenant administrator deactivates an application that's registered in
Microsoft Entra ID (formerly Azure Active Directory). This action invalidates any service principal
connections associated with the application because it can no longer issue tokens.

You might also receive the following error message:

  The service principal for resource '<ResourceID>' is disabled. This indicate that a
  subscription within the tenant has lapsed, or that the administrator for this tenant has
  disabled the application, preventing tokens from being issued for it.
---

Solution
To resolve this problem, the tenant administrator has to reenable the application or create a
new service principal connection.


Conditional Access policy mismatch for embedded
flows occurs
Connections can appear to be broken when you access a flow from an embedded surface (such
as a SharePoint list, Microsoft Teams channel, or Excel workbook) if the Conditional Access (CA)
policies for the host application and Power Automate have different requirements.

You might receive an authentication error message that resembles the following example:

   AADSTS50076: Due to a configuration change made by your administrator, or because you
   moved to a new location, you must use multi-factor authentication to access '<Resource>'.



Cause
When a user accesses a flow from SharePoint, Teams, or Excel, the host application exchanges
its token for a Microsoft Flow Service token. If the CA policies have different requirements
(MFA, Terms of Use, or device compliance) for one application but not the other, this exchange
fails.

This problem typically occurs if CA policies target individual applications that have different
requirements, instead of using the Office 365 app or All cloud apps target that covers both the
host application and Power Automate consistently.


Solution
    1. In the Microsoft Entra admin center    , go to Protection > Conditional Access > Policies.
    2. Switch your policy to target the Office 365 app or All cloud apps for consistent
         enforcement across Power Automate and the apps that embed it.
    3. If you must target individual applications, verify that all Conditional Access requirements
         (MFA, Terms of Use, device compliance) are consistent between the host applications
         (SharePoint, Teams, Excel) and Microsoft Flow Service (Application ID: 7df0a125-d3be-
         4c96-aa54-591f83ff541c ).

    4. Ask affected users to sign out and sign back in.
---

For more information, see Conditional access and multifactor authentication in Power
Automate.


Terms of Use policy breaks flow connections
Connections can break when an administrator adds a Terms of Use requirement to a
Conditional Access policy after flows are already running, or when a Terms of Use consent
expires on a recurring schedule.

You might see the following connection status:

  Failed to refresh access token for service


The accompanying error message doesn't specifically mention Terms of Use as the cause.


Cause
Power Automate connections refresh tokens silently in the background. When a Terms of Use
grant control is in scope, the silent token refresh fails because the Terms of Use acceptance
page can't be presented without an interactive session. This failure breaks connections
retroactively, even for flows that were working before the Terms of Use policy existed.


Solution
   1. Check Microsoft Entra sign-in logs for AADSTS50158 or AADSTS53003 errors that target the
     Microsoft Flow Service resource. On the Conditional Access tab, look for a Terms of Use
     grant control that have a status of Not Satisfied.
   2. Ask the flow owner to sign in interactively to the Power Automate portal    to accept the
     Terms of Use prompt.
   3. Repair or re-create the affected connection.
   4. To prevent recurrence, exclude service accounts and dedicated flow connection owners
     from Conditional Access policies that include Terms of Use grant controls.

For more information, see Conditional access and multifactor authentication in Power
Automate.


Related content
     Manage connections in Power Automate
---

     Create a connection with a service principal



Last updated on 03/31/2026
---


## Troubleshoot Power Apps flow integration

Troubleshoot Power Apps flow integration
issues
10/21/2025


Applies to: Power Apps
Original KB number: 4477072

When integrating Power Automate flows with Power Apps, you might encounter connection
reference errors, authorization errors, or triggers that don't fire, causing the flow to fail. This
article helps you troubleshoot these issues and provides best practices for managing flow
updates.

Flow integration errors typically occur when:

     Flow metadata becomes out of sync with your app
     Connection permissions are insufficient or misconfigured
     Flows are disabled or timed out
     Flow definitions change after app deployment

This document covers the following error codes along with their causes and mitigation
strategies:

     InvokerConnectionOverrideFailed
     ConnectionAuthorizationFailed
     WorkflowTriggerIsNotEnabled
     ResponseTimeout
     0x80040265/0x80048d0b
     MissingConnectionReference
     NotAllowedConnectionReference



Error code "InvokerConnectionOverrideFailed" on
Power Automate flow run
Some Power Automate flows might fail to run in Power Apps and you might see an error that
resembles the following in the Power Automate flow run history or the Power Apps telemetry:

  Output


       {
          "code": "InvokerConnectionOverrideFailed",
          "message": "Failed to parse invoker connections from trigger 'manual'
  outputs. Exception: Could not find any valid connection for connection reference
---

  name '<some_connection>' in APIM tokens header."
      }




  ７ Note

  This error might also occur when you call the install API on Dataverse (formerly Common
  Data Service), resulting in a generic error message: "Install flow failed."



Cause
This issue occurs when the Power Automate flow is updated to use a new connection, but the
app still uses the old flow metadata. Even though the flow is updated, the apps that reference
the flow still retain the previous flow metadata.


Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.


To resolve this error, manually edit the app so changes appear in the app and the flow works.

   1. Open the app for editing using the latest version of Power Apps Studio.
   2. Remove the Power Automate flows from the app.
   3. Readd the flows to the app.
   4. Save and republish the app.



Error code "ConnectionAuthorizationFailed" on
Power Automate flow run
  Output


       {
          "code": "ConnectionAuthorizationFailed",
          "message": "The caller with object id '{user_id}' does not have the
  minimum required permission to perform the requested operation on connection
  '{some_connection_id}' under API '{some_connection_api}'."
      }
---

Cause
This error means that the maker doesn't have permissions to the dependent connections that
are used in the flow actions. This error can occur even if the maker has permissions to the
Power Automate flow itself. This issue is a limitation of the Power Apps and Power Automate
flow integration.


Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.


To mitigate this issue, ensure that all connections used in the Power Automate flow are
authorized for the user who is adding the flow to the app. The user must have the necessary
permissions for each connection referenced by the Power Automate flow. For more
information, see Understand flow ownership and access.



Error code "WorkflowTriggerIsNotEnabled" on
Power Automate flow run
  Output


       {
          "code": "WorkflowTriggerIsNotEnabled",
          "message": "Could not execute workflow '<GUID>' trigger 'manual' with
  state 'Disabled': trigger is not enabled."
      }




Cause
The Power Automate flow is disabled or turned off.


Mitigation steps

  ７ Note
---

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.


Ensure that the Power Automate flow is turned on and verify the flow run by testing it
manually.



Inner error code "ResponseTimeout" on Power
Automate flow run
  Output


            {
              "error": {
              "code": 504,
              "source": "<api hub source>",
              "clientRequestId": "<GUID>",
              "message": "BadGateway",
              "innerError": {
                  "error": {
                      "code": "ResponseTimeout",
                      "message": "The server did not receive a timely response from
  the upstream server. Request tracking id '<some_tracking_id>'."
                      }
                  }
              }
          }




Cause
This error indicates that a synchronous Power Automate flow run exceeds the maximum
allowed execution time of 120 seconds (2 minutes), resulting in a timeout. Learn more about
the timeout limit of an outbound synchronous request.


Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.
---

To mitigate this issue, identify which Power Automate flow runs are exceeding the timeout limit
and optimize the flow's actions to complete within 120 seconds. Review the recommendations
in Troubleshoot slow running flows.



Error code "0x80040265" or "0x80048d0b" on
Power Automate flow run
  Output


       {

              "code": " 0x80040265",
              "message": "Failed to install the flow."

       }
       {

              "code": " 0x80048d0b",
              "message": "Failed to install the flow."

       }




Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.


Try the mitigation steps described for the following error codes, as the underlying causes might
be similar:

     WorkflowTriggerIsNotEnabled
     ConnectionAuthorizationFailed
     InvokerConnectionOverrideFailed



Error code "MissingConnectionReference" on
Power Automate flow run
  Output
---

       {
          "code": " MissingConnectionReference' ",
          "message": " Connection reference '<connection name>' was not given by
  invoker."
      }



Example error:

  Connection reference '<connection name>' was not given by invoker.


Cause
Power App and Power Automate flow metadata must always be synchronized. When changes
are made to a Power Automate flow, the app maker must edit the apps that use the flow to
remove or readd the changed flow.

For apps or flows included in a solution, an app might successfully invoke the flow in the
source environment but fail in the target environment with this error message:

  Connection not configured for this service.


This error occurs when the flow in the target environment has changes that aren't present in
the source environment, leading to mismatched connection references or metadata.


Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.


   1. In the source environment, edit the app. Remove and then readd the flows to the app.
     Save and publish the changes.

   2. In the target environment, remove all unmanaged solution layers from the app and flow.

   3. Export the solution and import it into the target environment.


       ７ Note
---

       Ensure that both the flow and the app have no unmanaged solution layers.
       Unmanaged solution layers can interfere with connection references and cause
       integration issues.




Error code "NotAllowedConnectionReference" on
Power Automate flow run
  Output


       {
          "code": " NotAllowedConnectionReference",
          "message": "Connection reference '<connection name>' was not given by
  invoker."
      }



Example error:

  Connection reference '<connection name>' was not given by invoker.


Cause
This error occurs when the app's flow metadata expects a specific connection reference (such
as a SQL connection) during installation. If flow's current metadata doesn't match this
expectation, an error occurs.


Mitigation steps

  ７ Note

  Make sure to perform the following steps in the source or development environment and
  update the solution. After you update the solution in the source or development
  environment, export and import it into all target or production environments.




Mitigation option 1

Reset the Power Automate flows in the app:

   1. In the source environment, edit the app. Remove and then readd the flows to the app.
     Save and publish the changes.
---

   2. In the target environment, remove all unmanaged solution layers from the app and flow.

   3. Export the solution and import it into the target environment.


        ７ Note

        Ensure that both the flow and the app have no unmanaged solution layers.
        Unmanaged solution layers can interfere with connection references and cause
        integration issues.




Mitigation option 2
Change the connection from Embedded to Invoker:

   1. To edit and update the flow settings, navigate to the Power Automate flow portal.
   2. On the flow details page, in the Run-only user section, select Edit.
   3. To update the flow connection source to Invoker, select Provided by run-only user and
     save.
   4. Verify by triggering the flow.



Failures caused by Power Automate flow updates
When flow updates cause integration problems, you might see these other symptoms that can
help you identify and troubleshoot the specific issue.


Symptom 1
When new input is added to a Power Automate flow but the Power App isn't updated, the flow
might fail. If the flow fails, it returns an error message that resembles the following example:

  Unable to process template language expressions in action
  'Send_me_a_mobile_notification' inputs at line '1' and column '1900': 'The template
  language expression 'triggerBody()['Sendmeamobilenotification_Text']' cannot be evaluated
  because property 'Sendmeamobilenotification_Text' cannot be selected. Please see
  https://aka.ms/logicexpressions for usage details.'.
---

                                                                                             



Symptom 2
If the connections required to run a Power Automate flow change, you might receive an error.

In Power Apps, it might look like:




In Power Automate flow, it might look like:

  Unable to process template language expressions in action 'Send_an_email' inputs at line
  '1' and column '1899': 'The template language expression
  'json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$connections']
  ['shared_office365']['connectionId']' cannot be evaluated because property
  'shared_office365' doesn't exist, available properties are 'shared_flowpush'. Please see
  https://aka.ms/logicexpressions for usage details.'.
---

                                                                                             



Symptom 3
If a response output is removed, Power Apps treats the value as blank and the app behaves
unexpectedly.


Cause
Power Apps needs to know three things to invoke a flow: what inputs the flow requires, what
connections to provide, and what outputs the flow returns. Power Apps stores this information
in your app definition, creating a binding between your app version and the flows it uses.
When you change any of these three flow aspects, you can break all previous app versions that
integrate with that flow.

Types of changes most likely to break a Power Apps ability to call a Power Automate flow
include:

   1. Adding a new Ask in Power Apps token.




                                                                                             


   2. Adding a new connection. For example, by adding a new action from a Connector that
     wasn't previously used like the SharePoint connector.
---

  3. Changing an existing connection. For example, changing an existing connection to a new
     connection.




  4. Removing an output from a Respond to Power Apps action.




Other changes to the inputs or outputs might not break the integration between Power Apps
and the Power Automate flow. However, the app must be updated to recognize and utilize new
or modified inputs and outputs.


Resolution
---

To fix an affected app or use these flow changes, you need to update the app. The approach
you take to resolve the issue depends on whether you're working with a live app or a
development version. Each scenario requires different steps to prevent disruption to users.


Changing a published (live) Power App
When your app is already published and in use, always create copies of flows before making
updates. Updating flows directly can break the app for existing users.

Follow these steps:

   1. Create copies of the flows you need to update using the Save As option.




   2. Make your changes to the copied flows.

   3. Update your app to use the new flows instead of the original ones.

   4. Test and publish the updated app.

   5. After all users upgrade to the new app version, you can safely delete or turn off the
     original flows.

This approach ensures users continue working with the original app and flows until they're
ready to use the updated version.
---

Changing a development version Power App
When you're still developing your app (not yet published), you can safely update flows directly
without creating copies.

Follow these steps:

   1. Make your changes to the flow (inputs, outputs, or connections).
   2. In Power Apps Studio, go to the Flows pane.
   3. Remove the flow from your app.
   4. Add the updated flow back to your app.
   5. Save your app.

This process updates your app to use the flow's new configuration. Since the app isn't
published yet, your changes don't affect users.



References
     Use Power Automate pane
---


## Troubleshoot HTTP 0 responses and other blocked calls

Troubleshoot HTTP 0 responses and other
blocked calls in Power Apps
Applies to: Power Apps, Power Automate


Summary
This article helps you investigate Power Apps and Power Automate calls that don't reach the
service or that return an error from an intermediary device. Typical failures include an HTTP status
of 0 , a proxy-issued status such as 403 , 407 , 502 , or 503 , and a request that's marked as
(failed) or (canceled) . Learn how to tell whether the failure originates on the client side or in

the network path, capture the right diagnostics, and work with your network team on a fix.


Symptoms
A connector or web request fails before the Power Platform service can return a successful
response. The failure is often intermittent and creates one of the following conditions:

      An HTTP status code of 0 in the Power Apps Live Monitor tool, in flow run history, or in
      browser developer tools. The response typically contains no body, no headers, and no
      meaningful error message.

      A request that has a displayed status of (failed) or (canceled) on the Network tab of
      browser developer tools.

      An HTTP status that's returned by an intermediary device (for example, a Zscaler, Netskope,
      or corporate proxy block page) instead of by Power Platform. For example:
          403 Forbidden

          407 Proxy Authentication Required

          502 Bad Gateway

          503 Service Unavailable


      Custom code that uses fetch or XMLHttpRequest and receives status: 0 or a generic
      network error.

All these symptoms share a common root pattern: The request is blocked or altered between the
client device and the Power Platform service instead of being processed and rejected by the
service itself.
---

Cause
An HTTP status of 0 isn't an actual response from the server. It means that the browser or client
never received a response from the remote endpoint. This condition usually occurs because the
request was blocked, dropped, or terminated before it could complete a round trip. Proxy-issued
statuses such as 403 or 407 mean something similar: An intermediary device intercepted the
request and returned its own response instead of forwarding the request to Power Platform.

Common causes include:

     Transient network outages or unstable device connectivity (for example, Wi-Fi drops, VPN
     disconnections, or cellular handoffs)
     Corporate proxies, firewalls, or SSL/TLS inspection devices that terminate, throttle, or silently
     drop the connection
     Network appliances that rewrite or strip CORS      headers (for example, changing Access-
     Control-Allow-Origin to a restrictive value) and cause browser-side failures before the

     network call finishes
     DNS resolution failures or DNS-based filtering that blocks the Power Platform service
     endpoint
     Secure web gateway or zero-trust products (such as Zscaler or Netskope) that intercept
     Power Platform traffic and block it, rewrite it, or return a custom error page
     Browser extensions (ad blockers, privacy tools) or local antivirus software that cancel the
     request before it's sent
     Browser local-network protections that treat proxied traffic as local-resource access and
     block the request
     The user navigating away, closing the tab, or putting the device to sleep before the request
     finishes


  ７ Note

  These failures originate on the client side or within your network path, not on the Power
  Platform service. Resolution usually requires coordination with your network administrator to
  identify why the request is blocked, redirected, or losing connectivity.



Determine the source of the problem
Verify that the request reaches the network
---

Use your browser's developer tools to inspect the failing call:

   1. In the browser, press F12 to open developer tools, and select the Network tab.

   2. Reproduce the issue in the app or flow.

   3. Locate the failing request. Look for responses that match one or more of the following
     indicators:

           Status 0 , (failed) , or (canceled)
           A 403 , 407 , or 502 response that doesn't resemble a Power Platform response

   4. Select the request, and examine the Headers section. Closely examine the Remote Address
     field. Also, review the response body for any indication that the request came from a proxy
     or security appliance instead of the service.

For "4xx" and "5xx" responses, inspect response headers for Power Platform service markers such
as x-ms-correlation-id or x-ms-request-id (with GUID values):

     If at least one valid x-ms-* request/correlation header is present, the request likely reached
     the service and was rejected there.
     If these headers are missing, and the response resembles a proxy or gateway page, an
     intermediary network device likely generated the response.

If you engage Microsoft Support, include any x-ms-correlation-id or x-ms-request-id values
that you captured. These identifiers help correlate the request with service telemetry.

The Remote Address field is one of the clearest signals:

     If the field shows an IP address and port (for example, 192.0.2.10:443 ), the request reached
     a remote server. The failure is then more likely a TLS, CORS, or service-side issue.

     If the field shows only a port (such as :443 or :80 ) together with no IP address, the
     connection was blocked, intercepted, or short-circuited before it left the device or local
     network. That strongly suggests that a proxy, firewall, DNS filter, or security agent (such as
     Zscaler) is handling the request locally instead of forwarding it. The same pattern often
     appears alongside a proxy-issued 403 or 407 response.
---

Capture an HAR file of the session so that you can share it with your network team.


Rule out device and connectivity problems
Before you engage your network team, rule out basic device and connectivity problems:

     Reproduce the problem on a different network (for example, a mobile hotspot) to check
     whether the problem follows the user, the device, or the corporate network.
     Try a different browser, or use an InPrivate or Incognito window by having extensions
     disabled.
     Verify that the device has a stable connection and isn't suspending Wi-Fi for power
     management.
     Test from a different device on the same network to isolate device-specific problems.

If the call succeeds on an alternative network but fails on the corporate network, the problem is
almost certainly in the corporate network path.

If failures affect users in only specific regions, also consider DNS response-size filtering by
intermediary devices. Some Power Platform host name chains produce larger DNS answers (for
example, because of CNAME expansion and geographic routing). Devices that enforce older DNS
size assumptions from RFC 1035       can block responses that are valid under RFC 6891       . The
result is region-specific app load or connector failures.


Work with your network administrator
The evidence might point to the corporate network. For example, you might notice missing
remote IP, or that failures occur only on the corporate network, or that other users are affected.
In these cases, engage your network administrator. Share the following information:

     The HAR file that you captured earlier
---

     The exact URLs of the failing requests (host name and path)
     The approximate time, user, and device where the issue occurred

Ask your network team to verify the following conditions:

     All required Power Platform endpoints are allowed end-to-end through proxies, firewalls,
     and SSL inspection devices. The authoritative list of host names and IP ranges is at Power
     Platform URLs and IP address ranges.
     DNS resolves Power Platform endpoints correctly.
     Allowlist rules cover dynamic host names and subdomains. Power Platform requests can use
     long, environment-specific host names under service domains instead of a single fixed host.
     A rule that allows only a previously observed subdomain can fail at the next routing change,
     even though no app logic changed.
     CORS headers returned by Power Platform are preserved end-to-end. Header rewrite or
     removal can cause browser-level failures (including HTTP status 0 ), even if endpoint allow-
     listing is otherwise correct.
     Inspection devices support larger DNS responses and EDNS behavior. This condition is
     especially important if failures are concentrated by region or office location.
     Secure all allowlist Power Platform host names in web gateways (Zscaler, Netskope, or
     similar), and protect them from SSL/TLS inspection. SSL inspection is a frequent root cause
     of HTTP 0 responses and unexpected 403 or 502 errors. The inspection device can break
     long-lived or chunked connections that the connector runtime relies on. It can also return
     its own block page if a policy match occurs.

If you suspect browser local-network protections, review the relevant browser guidance. For
Chromium, see Private Network Access: introducing preflights       .


Collect additional diagnostics
If the issue persists after the network team verifies the configuration:

     Capture a network trace (for example, with Wireshark       or pktmon on Windows) during a
     failing call.
     Use the Power Apps Live Monitor tool to verify whether the failure is consistent across
     requests or limited to specific connectors.
     Review HAR entries for proxy-identifying headers such as Via .
     Look for protocol downgrade patterns, such as HTTP/1.1 responses where you expect
     modern HTTP/2 . Connector traffic should use modern HTTP. Therefore, repeated
---

      downgrades often indicate intermediary inspection or proxy fallback, and they can affect
      reliability and performance.
      If a browser local-network access prompt appears, or if it appears that access was denied,
      collect that detail for the network team. Some proxy designs that use nonroutable or private
      address ranges can trigger local-network protections and block requests.
      Note whether the failures correlate with specific times of day, specific users, specific
      geographic locations, or specific connectors. This information often helps your network
      team pinpoint the device or policy that's responsible.


Solution
Your IT or network team usually makes most fixes. Share the HAR file and proxy logs that you
captured, and then apply one or more of the following changes:

      Allow the Power Platform URLs and IP address ranges through all proxies, firewalls, and DNS
      filters.
      Bypass SSL/TLS inspection for Power Platform host names on Zscaler, Netskope, or similar
      gateways.
      Stabilize device connectivity (Wi-Fi, VPN, cellular) for affected users.
      Review and reconfigure browser extensions or endpoint security products that cancel or
      rewrite requests to Power Platform endpoints.

If the problems continue after you make these changes, collect updated traces, and continue to
troubleshoot together with your networking and security teams.


Related content
      Troubleshoot broken connections in Microsoft Power Platform
      Managed connectors outbound IP addresses

Third-party information disclaimer

The third-party products that this article discusses are manufactured by companies that are
independent of Microsoft. Microsoft makes no warranty, implied or otherwise, about the
performance or reliability of these products.



 Last updated on 06/05/2026
---


## Troubleshoot Power Query issues

Troubleshoot Power Query issues
When you use Power Query for Excel to create a custom table that contains data from external
sources, you may receive the following error:

  "Your Microsoft Entra administrator has set a policy that prevents you from using this
  feature. Please contact your administrator, who can grant permissions for this feature on
  your behalf."


The error appears if Power Query can't access the organization's data in Power Apps or
Microsoft Dataverse. This situation arises under two sets of circumstances:

     A Microsoft Entra tenant administrator has disallowed users' ability to consent to apps
     that access company data on their behalf.
     Using an unmanaged Active Directory tenant. An unmanaged tenant is a directory
     without a global administrator that was created to complete a self-service signup offer. To
     fix this scenario, users must first convert to a managed tenant and then follow one of the
     two solutions to this issue. The solutions are described in the next section.

To resolve this issue, the Microsoft Entra administrator must follow either of the procedures
that are presented later in this article.



Allow users to consent to apps that access
company data
This approach is perhaps easier than the next, but it allows for broader permissions.

   1. In the Azure portal   , open the Microsoft Entra ID pane, and then select User settings.
   2. Next to Users can consent to apps accessing company data on their behalf, select Yes,
     and then select Save.



Allow Power Query to access company data
As an alternative, the tenant administrator can give consent to Power Query without modifying
tenant-wide permissions.

   1. Install Azure PowerShell.
   2. Run the following PowerShell commands:

            Login-AzureRmAccount (and sign in as the tenant admin)
---

            New-AzureRmADServicePrincipal -ApplicationId 00001111-aaaa-2222-bbbb-
           3333cccc4444


The advantage of this approach (versus the tenant-wide solution) is that this solution is very
targeted. It provisions only the Power Query service principal, but no other permission changes
are made to the tenant.



Update personal data
Users can update mashups and other information (such as query names and mashup
metadata) through the Query Editor and through the Options dialog box that's accessible from
the Query Editor.

In Power Apps, you access the Query Editor by doing the following:

   1. Go to the Data pane, expand it, and then select Tables.
   2. Select the ellipsis (...), and then select Edit Queries.
   3. In the ribbon, select Options, and then select Export Diagnostics.



Delete personal data
Most data is deleted automatically within 30 days. For data and metadata around mashups,
users must remove all their mashups through Power Apps. All of the associated data and
metadata will be deleted within 30 days.

To remove mashups from Power Apps:

   1. Remove the Data Integrator projects, which can be removed from the namesake tab.
   2. Select the ellipsis (...), and then select Delete.

If you created a mashup through the "New tables from data (Technical Preview)" feature, you
can remove it by doing the following:

   1. Select the ellipsis (...), and then select Edit queries.
   2. In the ribbon, select Options.
   3. Select Remove all queries.
     After you confirm that you want to delete your queries, they are deleted.



Export personal data
To export personal data, users can do the following:
---

   1. Open the Query Editor.
   2. In the ribbon, select Options.
   3. Select Export Diagnostics.

In Power Apps, you can access the Query Editor by doing the following:

   1. Go to the Data pane, expand it, and then select Tables.
   2. Select the ellipsis (...), and then select Edit Queries.
   3. In the ribbon, select Options, and then select Export Diagnostics.

System-generated logs about user actions on the user interface (UI) can be accessed in the
Azure portal.



 Last updated on 04/02/2024
---


## Common issues and resolutions for Power Apps

Common issues and resolutions for Power
Apps
ﾃ   Summarize this article for me




Summary
This article provides solutions to common problems that you might encounter when you create
or use Power Apps. The article organizes problems by functional area, such as connectors,
Power Automate integrations, Power Fx, and Power Apps Studio. Each section includes
troubleshooting steps and links to related documentation.

Before you troubleshoot specific problems, review Power Apps troubleshooting strategies for
guidance on how to identify the source of a problem. That article outlines key principles for
debugging both functional and performance problems.



Common Power Apps issue areas
     Connectors and delegation
     Power Automate Integration
     Power Fx
     Regional performance issues
     Power Apps Studio and Forms
     Browser performance
     Power Apps for Windows



Connectors and delegation
For an overview of how tabular and action connectors work, see Connections.

For details about delegation, see Understanding delegation in a canvas app.

For a description of how to monitor the data being sent and returned, see Debugging canvas
apps with Monitor.

     You don't have the correct permissions to use a connection.

     Users might encounter this message in two situations:

        The application shares an implicit connection that isn't a secure implicit connection. To
        resolve the problem, share the connection with the end user, but consider that this
---

   approach isn't recommended. The author should convert all connections to secure
   implicit connections.

   The application uses a secure implicit connection. In this case, republishing the app
   might resolve the problem.

Automatic Next links for galleries and grids don't work for action-based connectors.

Action-based connectors don't support next links. Next links are properties on query
results that allow a gallery or grid to automatically load the next set of results. For more
information, see Overview of connectors for canvas apps.

Sharing a Canvas app using SharePoint connector

For more information about how to share an app for SharePoint, see Connect to
SharePoint from a canvas app.

SQL data sources no longer add a [dbo] prefix to the data source name.

For more information about this change, see Connect to SQL Server from Power Apps.

Custom connectors and Microsoft Dataverse

You need to make adjustments if you built your app with Power Apps that:
   Is version 2.0.540 or earlier.
   Relies on a Dataverse database.
   Uses at least one custom connector from a separate environment.

First, deploy the custom connector to the same environment as the database. Then,
update the app to use the newly deployed connector. Otherwise, a dialog notifies users
that the API wasn't found. For more information, see Environments overview.

Column names with spaces

If you're using a list created using Microsoft Lists, a SharePoint library, or an Excel table in
which a column name contains a space, use single quotes with the column name, for
example someList.'Color Tag' .

Apps that connect to on-premises SharePoint

If you share an app that relies on connections that aren't automatically shared (for
example, an on-premises SharePoint site), users who open the app in a browser see a
dialog box with no text when they select or tap Sign in. To close the dialog box, select or
tap the close (X) icon in the upper-right corner.
---

  The dialog box doesn't appear if you open the app in Power Apps Studio or Power Apps
  mobile. For more information about shared connections, see Share app resources.

  For apps that are created from data, only the first 500 records of a data source can be
  accessed.

  Power Apps works with large data sources by delegating operations to the data source.
  For operations that can't be delegated, Power Apps shows a warning at authoring time
  and operates on only the first 500 records of the data source. For more information, see
  the Delegation overview.

  Excel data must be formatted as a table.

  For information about limitations when you use Excel as a data source, see Cloud-storage
  connections.

  Microsoft Lists is supported but not SharePoint libraries, some types of list columns, or
  columns that support multiple values or selections.

  For more information, see SharePoint Online.

  Sign-in issues on certain Android mobile devices when using authenticator

  On certain devices and in certain scenarios, you might experience sign-in failures when
  you use an authenticator. This problem happens because of a limitation that the OEM
  imposes. For more information, see ADALError:
  BROKER_AUTHENTICATOR_NOT_RESPONDING               .

  Apps cannot save null/blank values to data sources

  If your app can't save null or blank values to data sources, the Formula-level error
  management feature might be disabled. To fix this problem, go to Settings > Updates >
  Retired and make sure the Formula-level error management feature is enabled.



Power Automate integration
  Power Automate flows are orphaned in Power Apps.

  Power Automate flows that you add by using an older version of the Power Apps panel
  might become orphaned and removed. To fix this problem, re-add the flows manually.

  Power Apps custom pages (in a model-driven app) are out of synchronization with
  embedded Power Automate flow metadata.
---

     The metadata for a Power Automate flow might get out of synchronization with a model-
     driven app's custom page if you update the flow after embedding it. To update the
     metadata, follow these steps for each embedded flow:

        1. Edit the custom pages that use the flow.
        2. Open the Power Automate pane and refresh the flow.
        3. Save and republish the custom page.

     When you're done, follow these steps:

        1. Edit the model-driven app.
        2. Make a minor change to trigger the save option.
        3. Save and publish the model-driven app.



Power Fx
For more information about Power Fx, see Microsoft Power Fx.

     Connection.Connected returns the wrong value during OnStart in Power Apps for

     Windows.

     While offline, the Connection.Connected formula might wrongly return true immediately
     after starting an app in Power Apps for Windows. As a workaround, use a Timer control to
     delay the execution of the logic depending on it.

     Issues with Date-time

     For more information about date and time problems, see:
       Troubleshoot Canvas app date time issues
       Troubleshoot Model driven app date time issues



Regional performance
     Performance degradation when opening Power Apps Studio in China

     Power Apps Studio might take more than 30 seconds to load in China. This problem
     doesn't affect tenants that 21Vianet hosts locally.



Power Apps Studio and forms
The Power Apps Studio hosts the app editing and publishing experience.

     Problems with startup
---

If you have trouble accessing or starting Power Apps, see Troubleshooting startup or sign-
in issues for Power Apps.

Problems changing dimensions or orientation of SharePoint forms

If you have problems with the Screen size + orientation settings for custom SharePoint
forms, use the Custom size to work around the problem:

   1. Reset the setting by selecting the Small size.
   2. Toggle Orientation to Portrait and then back to Landscape.
   3. Select Custom and enter a desired screen size. For reference, the preset values are:
        "Width: 270, Height: 480" for the Small Portrait size.
        "Width: 720, Height: 480" for the Small Landscape size.

Copying and pasting screens across apps

Copying and pasting screens across apps isn't currently supported. To work around this
problem:

   1. Add a new screen to your target app.
   2. Copy the controls from the screen in your source app.
   3. Paste the controls into the screen of your target app.

Changing the layout of SharePoint forms

When you customize SharePoint forms in certain languages, if you try to change the
layout from Portrait (default) to Landscape, the app might show multiple errors (yellow
triangles in controls). To resolve these errors and retain the landscape layout, select Undo.

Changing a flow in a shared app

If you add a flow to an app and share the app, and then make changes to the flow, such
as adding a service or modifying a connection, more steps are required. You must also
first remove the flow from the shared app. Next, re-add the flow to the app. Finally, re-
share the app.

Changing a "Title" field in a table

If you change the Title field for a table that other tables reference through one or more
lookups, an error occurs when you try to save the change. To work around this problem:

   1. Remove any lookups to the table you want to change.
   2. Change the table's Title field.
   3. Re-create the lookups.

For more information about lookups, see Create a relationship between tables.
---

  When Power Apps generates an app from data, the field used for sorting and searching
  isn't automatically configured.

  To configure the field, edit the Items formula for the gallery, as described in Filter and sort
  a gallery.

  It can sometimes take a moment before a newly shared app can be used.

  In some cases, a newly shared app isn't immediately available. Wait a few moments, and it
  should become available.

  In the Form control, you can't change data by using a custom card.

  The stock custom card is missing the Update property, which is required to write back
  changes. To work around this problem:

     1. Select the Form control, and insert a card by using the right-hand pane based on
        the field that you want the card to show.
     2. Unlock the card, as described in Understanding data cards.
     3. Remove or rearrange controls within the card as you see fit, just as you would with
        the custom card.

  Card gallery is deprecated.

  Existing apps that use this feature continue to run for now, but you can't add a card
  gallery. Replace card galleries with the new Edit form and Display form controls.



Browser performance
  Browser running out of memory

  If you're using the 32-bit version of Google Chrome or Microsoft Edge and the browser
  runs out of memory while you're using Power Apps, consider using the 64-bit version.



Power Apps for Windows
  Power Apps mobile app for the Windows platform doesn't support the Dropbox
  connector.

  A pop-up dialog shows the following message in this situation:

    We can't connect to the service you need right now. Check your network connection
    or try again later.
---

      When this issue occurs, consider using a web player on the Windows platform.

      Microsoft Entra Conditional Access with the policy Require device to be marked as
      compliant doesn't work in Power Apps for Windows.

      When the Conditional Access policy is set to Require device to be marked as compliant in
      Microsoft Entra ID, users receive the following sign-in error and can't access their Power
      Apps.

        The application contains sensitive information and can only be accessed from devices
        or client applications that meet your enterprise management compliance policy.


      To work around the issue, they can use a browser.



Next steps
If your issue isn't listed in this article, you can search for more support resources , or contact
Microsoft support      . For more information, see Get Help + Support.



 Last updated on 02/26/2026
---


## Debug canvas apps by using Live monitor

Debug canvas apps by using Live monitor
and Trace

Summary
This article explains how to use Live monitor together with the Trace function to diagnose
problems in Microsoft Power Apps canvas apps. This approach helps you troubleshoot problems
that occur for only certain users or in specific environments. Live monitor shows real-time events
like network calls, data operations, errors, and performance details. The Trace function lets you
add custom diagnostic records to capture values from behavior formulas at key moments.


  ７ Note

  Live monitor isn't a practical option in every scenario, like SharePoint forms, custom portal
  embeddings, or problems that happen only intermittently. In those cases, see Debug canvas
  apps without Live monitor for alternative approaches.



Prerequisites
This article builds on Debugging canvas apps with Live monitor and Collaborative
troubleshooting using Live monitor. If you're new to Live monitor, review those articles before
you proceed.


Combine Live monitor and Trace
Live monitor shows platform-level activity: data operations ( getRows , createRow , patch ), control
evaluations, errors like the HTTP status codes 404 or 429 , timing, and delegation indicators.

When you add Trace calls in your behavior formulas ( OnSelect , OnVisible , OnStart ), you capture
context like:

     The user who's running the app
     The current environment
     The active screen
     Entity counts (rows in collections, related records)
     Business flags (VIP status, discount eligibility)
---

     Elapsed times for operations
     Any other information that helps you understand app behavior

Together, Live monitor and Trace answer both "what happened" and "why."


View data flowing over the network
Live monitor shows each data operation event by providing:

     Operation type ( getRows , createRow , patch , removeRow )
     Data source (Dataverse table or connector name)
     Timing (start, finish, duration)
     Result (success or error status code)
     Delegation hints (nondelegable operations trigger client-side processing)

To view the details, select an event. To understand why the operation occurred, correlate the
events with nearby Trace records. For example, a surge in getRows calls after a Trace operation
that includes the phase: "ApplyFilters" property might indicate an inefficient filter expression.


   Tip

  If you see HTTP 429 (throttling), review preceding events to check whether a loop or
  repeated evaluation triggered excessive operations. Optimize formulas or use collections to
  cache data and reduce network calls.



Use Trace effectively
The Trace function writes a structured record to Live monitor.

Key features:

     Works only in behavior properties ( OnSelect , OnChange , OnVisible , OnStart ).
     Accepts a text message and an optional record payload for extra details.
     TraceSeverity helps you filter events (Information, Warning, Error). Use Error sparingly.

     Has minimal performance effect when used appropriately. Remove or guard verbose Trace
     calls before you run a broad deployment.


Trace data property values by using debug buttons
---

Because you can't place Trace in data properties like a label's Text property, use temporary
debug buttons to capture those values.

To create a debug button:

   1. Add a button that's named btnDebugSnapshot and that has the Visible property set to
     Param("debug") = "true" .


     For more information about how to pass parameters, see Param function.

   2. In OnSelect , call Trace and include a snapshot record.

   3. When you test, add &debug=true to the app URL to show the button.


   Tip

  Trace the input values that you use to calculate a data property. These values often reveal
  why the result isn't what you expect.


The following example shows the Visible and OnSelect formulas for a debug snapshot button.


 powerfx

 // Visible property: Param("debug") = "true"
 // OnSelect:
 Trace(
     "Debug: Label value: " & Label1.Text,
     TraceSeverity.Information,
     {
         kind: "DataSnapshot",
         user: User().Email,
         customerCount: CountRows(Customers),
         productCount: CountRows(Products),
         maxPrice: Max(Products, Price),
         selectedProductId: If(!IsBlank(galProducts.Selected),
 galProducts.Selected.ProductId)
     }
 );




  ７ Note

  Guard debug controls by using query string parameters or role checks so that end users
  don't see them. Remove these controls before you finalize the app.
---

Debug checklist
Use this checklist when troubleshooting canvas app problems:

   1. Reproduce the problem with Live monitor open in Studio or in a published session.
   2. Add Trace calls at key phases (start, decision points, end, error handlers).
   3. Use query string parameters ( Param ) to tag the environment or show debug controls.
   4. Compare traces across users or environments. Look for different flags or counts.
   5. Correlate Trace events with network events (throttling, errors, extra calls).
   6. Remove or guard verbose Trace calls before you run a broad deployment.


Example scenarios
App works for one user but not another
User A submits orders successfully, but User B sees failures and different UI behavior, like a
disabled discount checkbox. You suspect the underlying data differs between their accounts.


Goal

Capture what the app sees about each user, including email, roles, customer selection, and
discount eligibility. Then, compare it with the data operations in Live monitor.


Steps

   1. Open the app in Power Apps Studio.
   2. Add Trace calls in the OnSelect property of the submit button.
   3. Save and publish the app.
   4. Open Live monitor for the published app.
   5. Select Connect user to invite User A. As User A runs through the app, you see both the
     built-in events and your custom Trace calls.
   6. Open a new Live monitor instance, and then connect User B in the same way.
   7. Compare the values to find the difference that causes the problem.


Example OnSelect formula together with Trace

 powerfx

 // Emit pre-submit context
 Trace(
     "Debug: Before Submit",
     TraceSeverity.Information,
---

         {
             user: User().Email,
             customerId: ddCustomer.Selected.Id,
             cartCount: CountRows(colCart),
             orderCountForCustomer: CountIf(Orders, Customer = ddCustomer.Selected),
             isVIP: ddCustomer.Selected.'VIP Flag',
             env: Param("env"),
             screen: App.ActiveScreen.Name
         }
  );

  // Perform data operations (simplified)
  ForAll(colCart,
      Patch(Orders, Defaults(Orders), {
          Customer: ddCustomer.Selected,
          Product: ThisRecord.Product,
          Quantity: ThisRecord.Quantity
      })
  );

  // Post-submit trace
  Trace(
      "Debug: After Submit",
      TraceSeverity.Information,
      {
          orderCountForCustomer: CountIf(Orders, Customer = ddCustomer.Selected)
      }
  );



Analyze the results

In Live monitor, filter by Trace events, button name, or search for "Debug:" in the event data.
Compare User A to User B:

       Do they have different isVIP values? This difference could change discount calculations.
       Are cart counts identical? If not, the upstream logic differs.
       Are error traces present only for User B? Expand the event to inspect the error details.

Correlate Trace events with adjacent getRows or patch operations. If User B triggers extra data
calls, like a nondelegable filter that forces multiple network requests, you see them in the event
table.


App works in one environment but not another
Your app works correctly in Test but fails in Production. For example, a gallery loads no items, and
submission is slow. Even though the app is the same, the data in each environment can differ.
Missing tables, different column values, larger datasets that trigger delegation limits, or
permission differences can cause the app to behave differently.
---

Goal

Gather environment-specific metadata and counts, and then compare the sequence and status
codes of data operations between environments. In this example, the app has one screen that
includes a form. This form contains a product that's selected from a gallery and that can be
updated. The update works in Test but fails in Production.


Steps

   1. Add an OnVisible Trace on the affected screen:


        powerfx

        Trace(
            "Debug: OnVisible on " & App.ActiveScreen.Name,
            TraceSeverity.Information,
            {
                recordId: varSelectedProduct.Id,
                hasDiscount: varSelectedProduct.HasDiscount,
                relatedOrders: CountIf(Orders, ProductId = varSelectedProduct.Id)
            }
        );


   2. Deploy the app with the new traces to production.

   3. Open Live monitor in Test, and then in Production. If necessary, export the logs.


Analyze the results

In the event list:

      Compare getRows events for Products across environments. Does one return zero results or
      error codes? A 404 code means the table is missing, 403 means access is denied, and 429
      means the requests are throttled.
      Look for repeated getRows calls. These calls might indicate a nondelegable formula.
      Compare the Trace values. Do products have different values for relatedOrders or
      hasDiscount ?


If you find a difference, add more Trace calls in which the variable is set, and then examine how
the calls are populated.

If you see network errors like 4xx responses, check that tables, flows, and connectors are set up
correctly in both environments.
---

Related content
      Debug canvas apps without Live monitor
      Advanced monitoring

）Note: The author created this article with assistance from AI. Learn more




 Last updated on 08/10/2026
---


## Debug canvas apps without Live monitor

Debug canvas apps without Live monitor

Summary
This article discusses alternative debugging approaches for Microsoft Power Apps canvas apps in
scenarios that don't support Live monitor. Use these techniques for SharePoint integrated forms,
custom pages, or custom portal embeddings in which you can't open Live monitor alongside the
app. It also covers intermittent issues that don't happen often enough to catch while Live monitor
is connected.

Live monitor is the recommended tool for debugging canvas apps because it shows real-time
events and works together with the Trace function. But some hosted or embedded scenarios
don't support it, and some issues occur too rarely to capture in a live session. This article covers
alternatives like Application Insights, Dataverse logging tables, SharePoint list logging, and on-
screen diagnostics panels.


  ７ Note

  For scenarios in which Live monitor is supported and available, see Debug canvas apps with
  Live monitor and Trace.



Alternative debugging approaches
If Live monitor isn't available, choose one of the following alternative debugging methods based
on your environment and needs.


                                                                                          ﾉ   Expand table


 Alternative            Best for                           Notes

 Application Insights   Centralized telemetry and          Requires Azure setup. Emits traces and metrics
                        performance monitoring             outside Power Apps.

 Dataverse logging      Ad-hoc diagnostics and audit       Create a custom table. Use guarded logic to
 table                  trails                             write records when debugging.

 SharePoint list        Lightweight environments without   Use Collect or Patch to write to a list. To
 logging                Dataverse                          control size, prune entries.
---

 Alternative            Best for                         Notes

 On-screen              Immediate feedback during        Only for secure audiences. Remove before a
 diagnostics panel      testing                          broad rollout.



Application Insights integration
Application Insights provides centralized telemetry for canvas apps. It captures performance
metrics, errors, and custom traces in Azure Monitor, where you can analyze data across sessions
and users.

This approach requires:

     An Azure subscription
     An Application Insights resource
     Setup in the Power Apps app settings

For setup instructions, see Analyze app telemetry using Application Insights.


Write debug records to Dataverse
To capture diagnostic information if your environment includes Dataverse, create a custom Debug
Logs table. This approach works well for ad-hoc troubleshooting and audit trails.


Create the Debug Logs table
   1. In Power Apps     , go to Tables, and create a new table that's named Debug Logs .
   2. Add the following columns:

             Title : A label for the log entry

             UserEmail : The email address of the user

             Timestamp : When the event occurred

             Payload : Additional data in JSON format

             Other columns as necessary for your scenario, like CartCount and ScreenName


Example: Write a debug record to Dataverse
Use a guarded Patch call to write records only if a debug query string parameter is present.


 powerfx
---

 If(Param("debug") = "true",
     Patch(
         'Debug Logs',
         Defaults('Debug Logs'),
         {
             Title: "BeforeSubmit",
             UserEmail: User().Email,
             CartCount: CountRows(colCart),
             Timestamp: Now(),
             Payload: JSON({customerId: ddCustomer.Selected.Id})
         }
     )
 );



Run the app in debug mode
To turn on debug logging, add &debug=true to the app URL. For more information about query
string parameters, see Launch and Param functions.

After you reproduce the issue, open the Debug Logs table in Dataverse to review the captured
records.


  ７ Note

  Remove or turn off debug logging before you deploy the app broadly. To manage storage,
  periodically delete old log entries.



Write debug records to SharePoint
For lightweight environments without Dataverse, use a SharePoint list to capture debug
information.


Create the debug list
   1. In SharePoint, create a list that's named AppDebugLogs .
   2. Add the following columns:

           Title : A label for the log entry

           UserEmail : The email address of the user

           Timestamp : When the event occurred

           Payload : Additional data in JSON format

           Other columns as necessary for your scenario
---

Example: Write a debug record to SharePoint

 powerfx

 If(Param("debug") = "true",
     Patch(
         AppDebugLogs,
         Defaults(AppDebugLogs),
         {
             Title: "BeforeSubmit",
             UserEmail: User().Email,
             Timestamp: Now(),
             Payload: JSON({customerId: ddCustomer.Selected.Id, cartCount:
 CountRows(colCart)})
         }
     )
 );




  ７ Note

  SharePoint lists have storage limits. To prevent the list from growing too large, regularly
  remove old entries.



Capture intermittent issues for later analysis
Some issues occur too infrequently to reproduce while Live monitor is connected. For these
issues, use Application Insights or a Dataverse or SharePoint logging destination to capture
diagnostic information each time the affected operation runs. Include enough context to
compare successful and failed attempts.

Add the following identifiers to each trace or log record:

     EntraObjectId : Use User().EntraObjectId to identify the user in Microsoft telemetry.

     SessionId : Use Host.SessionID to identify the specific app session and correlate it with

     server-side processing.
     Timestamp : Record when the operation occurred.

     Event : Identify the operation or stage, like BeforeSubmit or SubmitFailed .

     Relevant input and calculated values: Capture the values that control the behavior,
     especially intermediate values that might unexpectedly be blank.

For Application Insights, include these fields in the custom record passed to Trace .


 powerfx
---

 Trace(
     "BeforeSubmit",
     TraceSeverity.Information,
     {
         EntraObjectId: User().EntraObjectId,
         SessionId: Host.SessionID,
         ScreenName: App.ActiveScreen.Name,
         CustomerId: ddCustomer.Selected.Id,
         CalculatedRequiredValue: varRequiredValue
     }
 )


For a Dataverse table or SharePoint list, add EntraObjectId and SessionId text columns, and
then include the identifiers in each record, as shown in the following example.


 powerfx

 Patch(
     AppDebugLogs,
     Defaults(AppDebugLogs),
     {
         Title: "BeforeSubmit",
         UserEmail: User().Email,
         EntraObjectId: Text(User().EntraObjectId),
         SessionId: Host.SessionID,
         Timestamp: Now(),
         Payload: JSON(
             {
                 screenName: App.ActiveScreen.Name,
                 customerId: ddCustomer.Selected.Id,
                 calculatedRequiredValue: varRequiredValue
             }
         )
     }
 )


For example, suppose that form submissions fail for a small number of users because a required
field is blank. Log the inputs to the expression that calculates the field, the calculated result, and
the identifiers immediately before submission. Compare successful and failed records to check
which input or condition produces the blank value. If you have to open a Microsoft support
request, provide the Entra object ID, session ID, and timestamp for an affected attempt so that
support can correlate the event with Microsoft telemetry.


  ） Important
---

  Limit access to diagnostic data, and don't log passwords, access tokens, or other sensitive
  values. Remove or reduce verbose logging after you fix the issue.



Create an on-screen diagnostics panel
For immediate feedback during testing, create a diagnostics panel that shows debug information
directly in the app. This approach is useful if you need to see values in real time.


Collect debug data
Instead of using Trace , add data to a local collection, as shown in the following example.


 powerfx

 If(
     Param("debug") = "true",
     Collect(
         debugTraces,
         {
              Timestamp: Now(),
              Data: $"Before submit for {User().Email} with {CountRows(colCart)} items
 in the cart"
         }
     )
 )



Add a text control to show traces
Add a text control to the screen that shows the collected traces. Set the Visible property of the
text control so that the control appears only in debug mode.


Control properties

                                                                                       ﾉ   Expand table


 Property     Value

 Text         Concat(debugTraces, $"[{Text(Timestamp, "hh:mm:ss.fff")}] {Data}", Char(10))


 Visible      Param("debug") = "true"


 Height       200

 Width        300
---

 Property     Value

 X             Parent.Width - 320


 Y            20


This setup shows a scrollable list of debug messages that you can copy and analyze outside the
app.


Example YAML for the text control

If you use the YAML view in Power Apps Studio, apply the following configuration.


 YAML

 - TextDebugPanel:
     Control: Text@0.0.51
     Properties:
       Height: =200
       Size: =12
       Text: |-
         =Concat(
             debugTraces,
             $"[{Text(Timestamp,"hh:mm:ss.fff")}] {Data}",
             Char(10))
       Visible: =Param("debug") = "true"
       Width: =300
       X: =Parent.Width - 320
       Y: =20




  ） Important

  Remove or hide the diagnostics panel before you deploy the app to users. Users who open
  the app by using the debug parameter shouldn't see internal diagnostic information.



Best practices for alternative debugging
If you use an alternative debugging approach, follow these guidelines:

       Guard debug controls: Use query string parameters like Param("debug") = "true" or role
       checks to show debug features only during testing.
       Clean up before deployment: Remove debug controls, logging calls, and diagnostic panels
       before you run a broad deployment.
---

      Manage log storage: To manage storage for Dataverse or SharePoint logging, periodically
      delete old entries.
      Use meaningful labels: To make logs easier to analyze, include descriptive titles like
      "BeforeSubmit" or "OnVisible_OrderScreen."
      Include context: Log the user email, screen name, and relevant data values so you can
      correlate entries across sessions.


Related content
      Collaborative debugging with Live monitor
      Live monitor overview

）Note: The author created this article with assistance from AI. Learn more




 Last updated on 08/10/2026
---

Power Apps troubleshooting strategies
Article • 04/14/2025


There are different approaches to troubleshooting Power Apps depending on the type of issue
you're facing. The troubleshooting strategies in this article can help you narrow down the
cause of the issue and point you in the right direction to work around or fix the issue.



Functionality troubleshooting
For issues with functionality where Power Apps features aren't behaving as expected, try to
isolate the problem using the following steps and links as a guide. A critical step in figuring out
the issue is being able to reliably reproduce the issue in as few steps as possible.

As a first step, follow the General troubleshooting strategies.

Then, use the following articles to isolate the issue and create a minimal repro app, where
practical.

For Canvas apps:

      Isolate Canvas App issues
      Minimal Canvas App repro

For model-driven apps:

      Isolate Model App issues
      Minimal Model App repro

After you have isolated the issue to a specific functionality area, use the following sections to
help you work around or address the issue.

      Connectors and delegation
      Integration
      Power Fx
      Region
      Studio and Forms
      Browser
      Power Apps for Windows

If your issue isn't listed, see Next steps later in this article.



Performance troubleshooting
---

   Tip

  For performance issues, you can use profiling tools like Monitor and Performance
  insights to debug and diagnose problems.



Canvas apps
For more information, see Troubleshoot Power Apps canvas app performance issues.


Model-driven apps
For model-driven apps, verify if forms are designed for performance.

For more information on debugging model-driven apps and performance issues, see
Debugging model-driven apps with Monitor.



General troubleshooting strategies

Isolate changes
When you make multiple changes at the same time, it's not obvious which one causes a
problem. Try reverting to the last known working state and make a single change. If it works
fine, revert the change and make another one until the issue occurs. For example, you can
restore a canvas app to a previous version and apply changes progressively.

If you can't revert an app to a working state, it's also helpful to make one change differently
while keeping everything else the same.

Here are a few examples:

     If searching for a long piece of text doesn't return correct results, try a shorter piece of
     text.
     View the same app on the same device, but with a different browser.
     If the data isn't displayed correctly in a control, try displaying it in a different type of
     control.
     If the data isn't displayed correctly on a page, try a different page or app with the same
     data.
     If one data connection doesn't work, try another.
---

Knowing what works as expected is as important as knowing what doesn't. For example, if you
can connect to one Microsoft Dataverse table but not another, the table might be
misconfigured. On the other hand, if you can't connect to any tables at all, it could be a larger
problem caused by an outage, a network failure, or a bug. These possibilities suggest other
avenues for investigation and help you get closer to the source of the error.


Simplify
A complex app has many components that might go wrong. Remove unnecessary details so
that there are fewer variables.

If there are client scripts in model-driven apps, try disabling them. If the problem persists, at
least you have eliminated those scripts as the potential cause.


Start from scratch
Consider creating a new app or configuration. This process can be broken into multiple
simplified steps and checkpoints, especially when the original version is too complex to re-
create. Consider the essence of the app and experiment with what works and what doesn't. For
example, if a table in a model-driven app doesn't show the right records, try re-creating the
view.

If the new app works, compare it with the original one to find the difference. If there's no
difference, the problem might be fixed in the latest version. Or, the original app might have
configuration problems. Even if you can't upgrade your app, knowing if and how the problem
was fixed will guide the next steps.


Find out which layer has data issues
Power Apps is based on web technologies. Different layers are involved when working with
cloud data. Some typical layers are:

        Server - stores data and controls who can access it.
        Network - transports data between the server and the app.
        App - requests data from the server, processes it, and displays it in the app.
        App host - where the app is running. The host provides the infrastructure to use an app.
        For Power Apps, the app host can be a browser, Power Apps mobile, or another website
        that Power Apps is embedded in.

Together, these layers form a general technical stack for Power Apps. Isolating the layer where
a problem occurs can uncover more ideas for solutions and workarounds.
---

Here are some examples of isolating the layer:

     Server - if there's a problem with the server, the same issue will happen on any website or
     app that accesses the data. To investigate further:
        Check if you can work with data outside of Power Apps. For example, for Microsoft
        Lists, check if you can view and edit records on the SharePoint site that hosts the list.
        Check if a different user experiences the same problem. Comparing the experience
        with an admin user might uncover permission issues.
     Network - there won't be internet access when the network isn't available. Though
     unusual, check the following:
        Try a different network
        Try to run the app in a different geographical region, which might have different
        network conditions or restrictions.
     App - use Monitor to examine the network requests made by the app. If the correct data
     is returned by the server, it's a problem with the app. If the data returned is wrong, it
     might be a server error or the app didn't request the data correctly.
     App host - try a different host. For example, if you're using the Power Apps mobile app
     for Android, try the mobile app for iOS or use a desktop browser.


Reproduce intermittent issues reliably
Intermittent issues can be difficult to solve. The key is to create the conditions that make them
happen all the time. The following steps might help you investigate intermittent issues related
to caching, network speed, browser performance, or hardware limitations.



Try private browsing mode or a different browser
     Confirm that the browser you're using is up to date. For more information, see System
     requirements, limits, and configuration values for Power Apps.
     Expired cookies or stale files saved in a browser can cause incorrect operation. Try using
     the browser's InPrivate or Incognito mode.
     Try a different supported browser.
     Disable all browser extensions and add-ons.
     For apps, try reinstalling them to clear stale data.


Try a different network

Slow loading of data might result in different behavior. If you're using a mobile data
connection, try a wireless or wired connection. If you're using a virtual private network (VPN),
try disabling it. You can also simulate slow networks on desktop browsers with browser
developer tools.
---

Try a different device
Similar to data speed, processing speed can also result in different behavior. If you're using a
phone, check if the problem occurs on a desktop computer.



Next steps
If your issue isn't listed in this article, you can search for more support resources , or contact
Microsoft support    . For more information, see Get Help + Support.
---


## How to create a minimal repro canvas app

How to create a minimal repro canvas
app
Article • 04/02/2024


A minimal repro app is an app that contains the minimum amount of logic and controls
to reproduce a problem. This app helps you narrow down the source of the issue,
whether it be with the data source, formulas, or a particular configuration.

After creating a minimal repro app, you can download a copy of it and share it with
others, like in the Microsoft Power Apps Community        or with Microsoft Support   .

You can create a minimal repro app with one of the following methods:

      Create a blank app and add just the necessary connections and controls to
      demonstrate the problem.
      Make a copy of the original app, progressively remove irrelevant screens and
      controls, and simplify formulas until you're left with the issue's essence.



Replace external data sources
A minimal repro app should be self-contained. It shouldn't rely on connections to
external data sources, like Dataverse or SharePoint, because external parties won't be
able to access them.

You can see data sources used in the app in the Data panel.
---

To handle data sources when creating a minimal repro app, you can:

     Remove them if they're not relevant to the issue you're showing.
     Use Collections with sample data.
     Provide sample data in a csv or Excel file. Explain how to re-create the data source
     from scratch.

Sample data should be as simple as possible.



Stub integrations and external web services
Apps may use features from other web services. For example, it may display a Power BI
tile, YouTube video, or Power Automate flows.

Remove these components if they're not relevant to the issue you're showing. If they're
essential, you should provide materials and instructions on how to re-create them. Use
sample content instead of the original. If the issue doesn't occur with sample content, it
might be an issue with the external content or service. For example, a Power BI report
may not be configured correctly for embedding.



Simplify components
If the app contains components or code components, others may not be able to see
their internals or load them correctly.

Remove these components if they're not relevant to the issue you're showing. If they're
essential, you should simplify them as much as possible and then:

     Package them together with the app in an unmanaged solution
     Provide instructions on how to re-create these components from scratch.
     For code components, mention which lines of code and framework feature aren't
     working.



Review for privacy and security
Unauthorized users won't be able to access data sources in exported apps, but they can
see how the data sources are used in them. They can also see the app's controls and
formulas. If an entire solution .zip file is provided, assets like images are also visible.

Follow the below steps to help you limit privacy and security exposure before
distributing the exported app:
---

     Don't include private and confidential information in the app. Check names of
     variables, controls, and other app elements that can inadvertently give away
     sensitive information.
     Create a new app from scratch instead of simplifying an existing production app. A
     new app will also reduce the accidental exposure of sensitive information if you
     were to use the original app instead. You'll save time by not needing to manually
     remove sensitive information from the original app.
     Distribute just the .msapp file instead of the .zip file. The .msapp file can be found
     inside the .zip package.



Download the minimal repro app
A canvas app can be saved in a .msapp or .zip file, depending on how it was created.


Power Apps
   1. Sign in to Power Apps     .

   2. Open the app for editing.

   3. Expand the Save menu item and select Download a copy.




     The downloaded .msapp file can be opened by others selecting Open in the menu
     bar of Power Apps    . You may have to expand the menu bar to see this option.
---

Microsoft Lists
  1. Open the list.

  2. Select Integrate > Power Apps > Customize forms. The customized form will open
    in Power Apps.




  3. Select Share from the menu at the top. The details page with the sharing panel will
    open.




  4. Dismiss the sharing panel.

  5. Select Export package in the menu bar.




  6. Type a name to the package. Review the exported content and select Export.

    The downloaded .zip file can be opened by others.


Power Apps in Teams
  1. In Microsoft Teams, go to the Power Apps app list for your team.

  2. Select the app.

  3. Select Export solution from the menu at the top.
---

   4. Review the exported content and select Export as zip.

     The downloaded .zip file can be imported by other users.


Custom pages
Only custom pages in unmanaged solutions can be exported. If the custom page is in a
managed solution, ask the publisher of the solution to create an unmanaged solution
that contains the custom page. You can also create a new unmanaged solution and
custom page there.

You can export custom pages in an unmanaged solution just like any other solution
component. The downloaded .zip file can be imported into any environment by other
users.



Next steps
     Ask a question with Microsoft Power Apps Community
     Get Microsoft Support



See also
     Debugging canvas apps with Monitor
     Debugging model-driven apps with Monitor




Feedback
---

Was this page helpful?      Yes    No


Provide product feedback
---


## Isolate issues in canvas apps

Isolate issues in canvas apps
Article • 04/02/2024


Canvas apps allow you to design apps with numerous different visuals and various data
connections. Use IntelliSense and the App checker       as guards against common issues.
Monitor and the Variables panel can help you with debugging.

Here are some other techniques to isolate problems in a canvas app.



Inspect formulas with debug labels
Formulas can be complex. When things go wrong, it can be difficult to pinpoint which
part failed. Debug labels are a useful technique to see the results of different parts of a
formula.

A debug label is a Label with its Text property set to a formula of interest. It lets you see
exactly how Power Apps treats these formulas. To avoid scoping bugs, insert the debug
label outside other controls like Gallery and Form.

Imagine that a Combo box control is showing less than expected and the dropdown
options are blank.




Check if the Combo box is configured correctly. For example, the Items property is set
to a complex formula below:

  Power Apps


  AddColumns(
    GroupBy(
      Filter( Products, Rating > 4 ),
      "ProductType",
      "Details"
    ),
    "Total quantity",
---

      Sum( Details, Quantity )
  )



Start with the innermost expression Filter( Products, Rating > 4 ) . Insert a debug
label and set its Text property to test the result of that expression. Some useful
information to verify:

      Check if the number of results is as expected: CountRows( Filter( Products,
      Rating > 4 ) )

      Examine the first result and verify the filter is working as expected: "Rating of
      first result is " & First( Filter( Products, Rating > 4 ) ).Rating

      Check results by combining their names: Concat( Filter( Products, Rating > 4 ),
      ProductName & ", ")



   Tip

  When working with datasets, debug tables are useful for previewing records. The
  concept is similar to debug labels. Insert a Data table with its Items property set to
  the dataset of interest.

  You might want to use the FirstN and LastN functions for better performance with
  datasets.


Once you've confirmed that an expression is evaluated correctly, you can move on to
the next outer expression GroupBy( Filter( Products, Rating > 4 ), "ProductType",
"Details" ) . By proceeding methodically, you can find out which part of a complex

expression isn't working.

When using empty dropdown options, start with the DisplayFields property. Imagine it's
set to [ProductType] . Use a debug label to verify that this field is recognized by Power
Apps and contains text. Since all the dropdown options are empty, it's sufficient to
examine any record. Let's pick the first record and see what its ProductType field is. Set
the debug label to:

  Power Apps


  First(
    AddColumns(
      GroupBy(
        Filter( Products, Rating > 4 ),
        "ProductType",
        "Details"
      ),
---

       "Total quantity",
       Sum( Details, Quantity )
    )
  ).ProductType



If the result is empty, it could be:

     The ProductType field for that record really is empty. If the dataset comes from
     outside the app, check it outside of Power Apps.
     One or more of the expressions isn't working. Break it down as described above to
     narrow down. It could be a Power Apps bug or a mistake in writing the formula.
     Data isn't reaching Power Apps. It could be a networking issue, an issue with the
     data source, or a Power Apps bug.

If the result has text, then it's likely a Power Apps bug with the control. You can report
the bug through a support request and use a different control as a workaround.



Try a different control
To find out if the issue is with a specific control, try using a different control that has the
same data type of input or output.


Boolean
     Check box
     Toggle


Choice and Table
     Charts
     Combo box
     Data table
     Dropdown
     Gallery
     List box
     Radio


Date and DateTime
     Date picker
     Text input
---

Image and Media
     HTML text
     Image
     Image property of Audio, Video, and Microphone


Number
     Rating
     Slider
     Text input


Text
     Rich text editor
     Text input


All types
     Label, after converting a value to text

If the same problem happens on a different control, then the issue is with the formulas
or data source used. Proceed with the debugging steps above to further isolate the
issue.

If the problem only happens on a particular type of control, then it's likely a control bug.
You can report the bug to Microsoft.



Try a different app structure
Formulas can behave differently for controls inside another control. For example,
controls inside a Gallery can use ThisItem but controls outside the gallery can't. Controls
outside a Gallery or Component can't reference the controls inside.

This different visibility of identifiers is called scope. Controls that contain other controls
introduce a new scope.

     Component
     Container
     Display form
     Edit form
---

     Gallery
     Horizontal container
     Scrollable screen (Fluid grid)
     Vertical container

If a formula isn't working inside a contained control, it could be related to scoping. Try
using the same formula outside the container.

For example, a Label control inside a Gallery should show each record's name but no
text is appearing. Label.Text is set to ThisItem.Name . Gallery.Items is set to Products .




To check if it's a scoping issue, insert a debug label outside the Gallery, at the top-level
of the app. Set its Text property to show the name of the first record of the dataset:
First(Products).Name .


The debug label should have the same result as the first row of the gallery. If not, it's
likely a scoping bug with Power Apps that you can report through a support request. On
the other hand, if both are blank, then the issue could be with the data source.

Some possible workarounds for scoping issues:

     Move controls outside of their containers
     Refer to data in global or context variables
     Use Patch to avoid using an Edit form control
---

Restore to an earlier version
If you haven't made major changes to an app and it suddenly stopped working after
republishing it, try restoring it to the previous version. If it works again, examine the
changes made to see what might have broken the app.

Sometimes, bugs may be introduced with new versions of Power Apps. Conversely, new
versions may bring bug fixes. Microsoft Support can recommend whether you should
revert to an older authoring version or upgrade to a newer one. Remember there's
limited support for non-recommended versions if you change the authoring version on
your own.



Create a minimal repro app
The process of creating a minimal repro app may uncover app configuration errors that
aren't obvious with a complex app. Even if the problem isn't fixed, you would have
narrowed the cause and made it easier to explain the problem to others.



Next steps
Debugging canvas apps with Monitor



See also
General Power Apps debugging strategies




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot date and time issues in Power Apps canvas apps

Troubleshoot date and time issues in
Power Apps canvas apps
Article • 04/02/2024


When date and time values are off by a day or a few hours, it might be caused by time
zone or daylight saving adjustments. This article provides tips to troubleshoot issues
such as:

      The Date and Time field shows UTC instead of local time or vice versa.
      The Date Only value shows the wrong date for some users and time zones.
      Entering a daylight saving switchover date results in the date being off by one day
      or the time being off by an hour.



Determine if it's a server or client issue
Canvas apps are web apps. They get data from cloud services (servers). The same data
can power multiple apps (clients). Errors can occur on the server or client.

If the date and time value in the data source is unexpected, it will likely appear
incorrectly everywhere and not just in canvas apps. Therefore, verifying the stored value
is an important first step.


Check if the correct value is stored on the server

Date and time values are usually stored as UTC. For Dataverse tables, you can view the
raw date and time value with a Web API query. For other data sources like Microsoft List
or Excel, see their respective documentation.


Check the time zone adjustment settings of the data source and
Date Picker control

Some data sources have already been adjusted for time zones. In addition, the Date
Picker control can also adjust time zones with its DateTimeZone property.

A common mistake is mismatching the data source and control settings. For example,
when a Dataverse table column is Time-Zone Independent, but the Date Picker's
DateTimeZone is set to Local, the UTC value from the server will be displayed according
to the user's time zone. The reverse is also true. A User Local value from Dataverse will
be displayed as UTC when the DateTimeZone is set to UTC.
---

Note that this potential conflict doesn't occur with model-driven apps because it's
impossible to customize time zone handling for individual controls.



Try a different time zone
To find out if time zone and daylight saving adjustments are causing unexpected values,
try changing the user's time zone.

Canvas apps use the system time zone. For information on how to change it, see the
respective documentation in Windows, Android, iOS, or macOS.


   Tip

  The following methods provide more details to make it easier to investigate date
  and time issues.

        Show the user's time zone
        Change the "Date Only" format to "Date and Time"
        Don't use 2-digit years




Show the user's time zone
You can verify the user's time zone with the TimeZoneOffset function. It gives the
number of minutes between UTC and the user's time zone. For example, if the user is in
Pacific Standard Time, it will return 480. This is the same offset that the Date Picker
control and Power Fx use to adjust time zones and daylight savings.

With this offset, you can calculate whether the date and time values have been adjusted
correctly.



Change the "Date Only" format to "Date and
Time"
If a date-only value is off by a day, it's helpful to show the time part to see if time zone
adjustments could be the cause.



Don't use 2-digit years
---

The 2-digit year is ambiguous. For example, 40 might mean 1940, 2040, or 2140. How
the system interprets 2-digit years can and will likely change over time.

It's also difficult to investigate when the complete date and time values aren't shown.
For these reasons, it's strongly recommended to use 4-digit years, especially when
entering dates.



Common issues with Dataverse Date and Time
columns

"Date Only" column shows the wrong date for some users
This issue can occur for Time-Zone Independent and User Local adjustment behaviors,
which always have a time component. Time zone adjustments, either by Dataverse or
the canvas app, can move the date forward or backward by a day.

To solve this issue, show the time component of the value and check for time zone
adjustment settings.


Form shows a time picker for a column even though its format is
"Date Only"
This issue can occur for Time-Zone Independent and User Local adjustment behaviors,
which always have a time component. If you add such a column to a form, the form will
assume that you also need a time.

If you don't want users to see or edit the time component of the value,

     Remove the time picker.

     For User Local columns that don't need time zone adjustments, change their
     adjustment behavior to Date Only.


        ７ Note

        This is different from the Date Only format. This is a permanent change and
        can't be undone. Other apps, plugins, or workflows that previously adjusted
        the column for time zones might not work correctly.




See also
---

Behavior and format of the Dataverse Date and Time column




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Custom pages and client SDK script
don't load for Power Apps
Article • 11/30/2022


Applies to: Power Apps



Symptoms
Custom pages, the Microsoft 365 app launcher (also known as "the waffle"), or other
Power Apps components don't load. A network trace shows various issues that affect
calls with request URLs, such as:

      https://apps.powerapps.com/apphost/clientsdk?version=1
      https://content.powerapps.com/resource/webplayer/hashedresources/ikhj4ts3cqjq9

      /js/PowerAppsHostingSdk.bundle.v1.js




Cause
The content delivery network is blocked because of the firewall or network settings on
the client. Additionally, an AppHostClient SDK request fails and displays status code 0. In
this case, your organization receives the following error message:

  The script https://apps.powerapps.com/apphost/clientsdk?version=1 didn't load
  correct.



Resolution
To fix this issue, make sure that all services to which Power Apps Studio talks and their
usages are not blocked by the firewall or network settings.




Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

Filter expression returns extra blank
records in results
Article • 11/30/2022



Symptoms
Filter results sometimes have extra, unexpected, blank records in the result.



Cause
Client-side filtering can result in blank records in the result when the Formula-level
error management app setting is turned on. When a filter expression results in an
unhandled error, blank records may be inserted in the result.



Resolution
Use a formula pattern as follows:

  Power Apps


  Filter(datasource, IfError(<query predicate>, false))




See also
      Get started with formulas in canvas apps
      Formula reference for Power Apps




Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

"Something went wrong" error that occurs
when using the wrap feature
08/04/2025


This article provides solutions to error messages that occur when using the wrap feature in
Microsoft Power Apps. These errors often occur when steps in the wrap wizard, such as
permissions or registration, are missed, even if the build succeeds but login fails.



Error message: "Something went wrong. [5objp]"
This issue might occur due to a signature hash key mismatch or a redirect URI mismatch during
the app authentication process.


Cause 1: Signature hash key mismatch

The APK is signed with a different key than the one registered in the Microsoft Entra ID
application. This issue might occur if:

     A different keystore is used during the build process.
     The registered hash key is incorrectly generated or copied (for example, it includes extra
     spaces or invalid characters).

To resolve this issue, verify that the signature hash key is correct:

   1. Generate the correct hash key from the keystore used to sign the app.

   2. In the Microsoft Entra admin center     , go to App registrations and select your app.

   3. In the app's navigation pane, select Authentication.

   4. Under the Platform configurations section, locate the Android platform.

   5. Check if your app's signature hash key is listed and matches the hash key generated from
     your keystore.

   6. If the hash key is missing or incorrect, add or update it as needed, and then save your
     changes.


Cause 2: Redirect URI mismatch

The redirect URI being used by the app doesn't match what's registered in the portal:
---

     Redirect URIs are case-sensitive. Mismatches might occur if the Bundle ID or URI is
     entered with incorrect casing.
     Special characters in the URI (such as %2F and %3D ) must be properly encoded and match
     exactly what's registered in Microsoft Entra ID.

To resolve this issue, verify that the redirect URI is correct:

   1. Install Android Studio     and set up an emulator.

   2. Launch the emulator and drag the APK file onto it to install the app.

   3. Open the app in the emulator, attempt to sign in, and note the error message.

   4. On the error screen, locate the redirect URI being used.

   5. If the hash key in the URI contains encoded characters (for example, %2F ), decode them
     ( %2F becomes / ) to get the signature hash key.

   6. Copy the decoded signature hash key.

   7. In the Microsoft Entra admin center      , go to App registrations and select your app.

   8. Under Authentication, review the configured redirect URIs.

   9. If the redirect URI is missing, add it with the correct Bundle ID and signature hash key,
     and then save your changes.

  10. Compare the existing redirect URI character by character (including case and encoding)
     with the one registered in Microsoft Entra ID.

  11. If manually entering the Bundle ID in the portal, double-check for case consistency.


Recommended practices
To avoid this error in the future:

     Always copy the Bundle ID and hash key directly from the project or build output.
     Use logging or emulator logs to inspect the exact redirect URI at runtime.
     Avoid manually typing or modifying hash keys or redirect URIs.
     Use Android Studio        to verify your app configuration.



Error message: "Something went wrong [2002]"
and error code 9n155
---

The error might occur when the app registration isn't configured to support multitenant
accounts.


Cause

This error typically occurs when the app registration is created using the wrap wizard, which, by
default, sets the app to single-tenant mode. If the user doesn't manually update this setting or
accidentally selects single tenant during manual app registration, the wrap app is unable to
authenticate, resulting in error code 9n155.


Resolution

   1. In the Microsoft Entra admin center      , go to App registrations and select your app.

   2. In the Essentials section, locate Supported account types. It should be set to Multiple
     organizations. If not, set it to Accounts in any organizational directory (Any Microsoft
     Entra directory - Multitenant).

   3. Save your changes.



Other issues
If your issue isn't covered here, or if the preceding steps don't resolve your problem, search for
more support resources     or contact Microsoft support       with detailed steps to reproduce the
problem.



Related information
     Azure key vault errors in wrap for Power Apps
     Troubleshoot common issues when using the wrap feature
---


## Troubleshoot common issues when using

Troubleshoot common issues when using
the wrap feature
08/04/2025


This guide provides solutions to common issues you might encounter when using the wrap
feature in Microsoft Power Apps.



Issue 1: Wrap build fails
If your wrap build fails, try the following actions:


Verify image formats
Ensure that all images in your wrap project are in PNG format. Using other formats can cause
the build to fail. Use an image converter to convert your images to .png format.


  ） Important

  Renaming a file extension to .png doesn't convert the image to PNG format.




Check Azure key vault setup
     Ensure you create an Azure service principal and assign the correct role.
     For more information, see Azure key vault for wrap in Power Apps.

Your key vault must contain:

     For iOS: two tags, one certificate, and one secret.
     For Android: one tag and one certificate.




Issue 2: Wrap button is disabled
Confirm you have edit permissions for the app and try again. For a list of requirements, see
Permissions and access requirements for wrap.
---

Issue 3: Unable to save your wrap project or trigger
a build
Update to the latest version of the wrap solution and try again.




Issue 4: Unable to install a wrapped mobile app
Ensure your app is properly signed by configuring a key vault during the build process or by
signing the app manually.

For more information, see:

     Set up Key vault for automated signing
     Code sign for iOS
     Code sign for Android

Additionally, verify your device meets the minimum requirements.




Issue 5: Can't sign in or see data in a wrapped app
If you can't sign in or see data in your wrapped app, try the following actions:


Verify API permissions and access
     Ensure all required API permissions are configured and that admin permissions are
     granted.
---

                                                                                             


   Ensure the Add-AdminAllowedThirdPartyApps script runs successfully.
   For more information, see Allow registered apps in your environment.


Check account types and redirect URIs
   Verify the Microsoft Entra app type is set to Multitenant and that the supported account
   type is Accounts in any organizational directory (Any Microsoft Entra ID tenant).

   Configure proper redirect URIs for iOS and Android:
      For Android, confirm the hash is correct.
      For more information, see Configure platform settings and redirect URIs.




Issue 6: Fail to sign in to a wrapped app
 1. Ensure the user has access to the app. For more information, see Share a canvas app with
   your organization.

 2. If the user has app access but still can't sign in, check the Conditional Access policies in
   the Microsoft Entra admin center.

 3. To troubleshoot sign-in errors, copy the correlation ID from the mobile screen where the
   sign-in failed and refer to How to troubleshoot Microsoft Entra sign-in errors to
   understand the error and the failed policies.

 4. Check Microsoft Entra authentication and authorization error codes.
---

Other issues
If your issue isn't covered here, or if the preceding steps don't resolve your problem, search for
more support resources     or contact Microsoft support     with detailed steps to reproduce the
problem.


Collect diagnostic information
For sign-in issues, you can collect session details and include them when you contact Microsoft
support:

     For the wrap wizard: On the sign-in screen, tap the gear icon in the upper-right corner
     and select Session Details.
     For mobile devices: After opening the app, press and hold the screen, and then select
     Session Details.
---


## Azure key vault errors in wrap for Power

Azure key vault errors in wrap for Power
Apps
08/04/2025


This article provides step-by-step solutions for Azure Key Vault errors you might encounter
when using the wrap wizard to build your mobile app.


                                                                                              ﾉ   Expand table


 Error       Error message
 code

 1000118     Default subscription not found or missing access permissions.

 1000119     Key vault doesn't exist or is missing access privileges.

 1000120     No organization ID tags found on key vault. Ensure that the tag {Bundle ID}.{organization-id}
             is present and uses the correct case sensitivity.

 1000121     Android keystore isn't valid. Ensure that the tag {Bundle ID}.{keystore} is present and uses the
             correct case sensitivity.

 1000122     iOS certificate isn't valid. Missing Tag and/or Secret. Ensure that the tag {Bundle ID}.{cert} is
             present and uses the correct case sensitivity.

 1000123     iOS profile isn't valid. Ensure that the tag {Bundle ID}.{profile} is present and uses the correct
             case sensitivity.

 1000128     Missing access key required to access the Azure Blob Storage location. Ensure that the tag
             {Bundle ID}.{accessKey} is present and uses the correct case sensitivity.

 1000130     Missing default value: The required environment variable for setting up Azure Key Vault in the
             wrap wizard isn't set.

 1000131     No tags or missing access permission for the specified Azure Key Vault.

 1000132     Missing environment variable 'PA_Wrap_KV_ResourceID' for the targeted environment.




Error code 1000118
Error message: Default subscription not found, or missing access permissions.



Resolution steps
   1. Ensure your Azure key vault is in the tenant's Default subscription.
---

2. As a Microsoft Entra ID (formerly Azure AD) admin, add the service principal for the
  AppID "4e1f8dc5-5a42-45ce-a096-700fa485ba20" by running the following commands in
  PowerShell:

    PowerShell


     Connect-AzureAD -TenantId <your tenant ID>
     New-AzureADServicePrincipal -AppId 4e1f8dc5-5a42-45ce-a096-700fa485ba20 -
     DisplayName "Wrap KeyVault Access App"



3. In the Azure portal   , under Access Control (IAM), assign the Reader role to your service
  principal:

   a. Go to Access control (IAM), and then select Add role assignment.




                                                                                          


  b. Choose Reader under Job function roles and go to the Members tab.




                                                                                          


   c. Search for your app name.
---

                                                                              


      d. Assign the Reader role.




                                                                              



Error code 1000119
Error message: Key vault doesn't exist or is missing access privileges.


Resolution steps
   1. Confirm your Azure key vault is in the tenant's Default subscription.

   2. While creating the key vault, select Vault access policy.
---

3. As a Microsoft Entra ID (formerly Azure AD) admin, add the service principal for the
  AppID "4e1f8dc5-5a42-45ce-a096-700fa485ba20" by running the following commands in
  PowerShell:

    PowerShell


     Connect-AzureAD -TenantId <your tenant ID>
     New-AzureADServicePrincipal -AppId 4e1f8dc5-5a42-45ce-a096-700fa485ba20 -
     DisplayName "Wrap KeyVault Access App"



4. In the Azure portal   , assign the Reader role as shown in the previous error code section.

5. Add access policies to the key vault:
---

Error code 1000120
Error message: No organization ID tags found on key vault. Ensure that the tag {Bundle ID}.
{organization-id} is present and uses the correct case sensitivity.


Resolution steps
   1. In the Power Platform admin center     , select your environment.




                                                                                         
---

   2. Copy the Organization ID.




   3. In your key vault, go to Tags and create a tag named organization-id with your
     organization ID as the value.




                                                                                            



Error code 1000121
Error message: Android keystore isn't valid. Ensure that the tag {Bundle ID}.{keystore} is present
and uses the correct case sensitivity.


Resolution steps
   1. Import your Android Certificate.
---

                                                                                     




                                                                                     


 2. Add a Tag for your certificate:

         Tag name: Use the same Bundle ID as your wrap project (for example,
         com.testApp.wrap ).

         Tag value: Use the certificate name you assigned when uploading (for example,
         AndroidCertificate ).




                                                                                     



Error code 1000122
---

Error message: iOS certificate isn't valid. Missing Tag and/or Secret. Ensure that the tag {Bundle
ID}.{cert} is present and uses the correct case sensitivity.


Resolution steps
   1. Import your iOS Certificate.




                                                                                            




                                                                                            


   2. Add a Tag for your certificate:

           Tag name: Use the Bundle ID from your wrap project.
           Tag value: Use the certificate name you assigned when uploading (for example,
            iOSCertificate ).
---

                                                                                              



Error code 1000123
Error message: iOS profile isn't valid. Ensure that the tag {Bundle ID}.{profile} is present and
uses the correct case sensitivity.


Resolution steps
   1. Import your Provisioning Profile as a Secret.

   2. Add a Tag for your provisioning profile:

           Tag name: Use the Bundle ID from your wrap project.
           Tag value: Use the name you gave the secret when uploading (for example,
           iOSProvisioningProfile ).




                                                                                              



Error code 1000128
Error message: Missing access key required to access the Azure Blob Storage location. Ensure
that the tag {Bundle ID}.{accessKey} is present and uses the correct case sensitivity.


Resolution steps
Add your access key from the Azure Blob storage account to the Azure key vault.

For more information, see Step 3: Choose target platform.
---

Error code 1000130
Error message: Missing default value: The required environment variable for setting up Azure
Key Vault in the wrap wizard isn't set.


Resolution steps
   1. Assign the resource ID of the Azure key vault you intend to use with your wrap
     application to the variable.

   2. Confirm that the specified resource ID includes all required tags associated with the
     Bundle ID defined in the wrap wizard.

For more information, see Step 3: Choose target platform.



Error code 1000131
Error message: No tags or missing access permission for the specified Azure Key Vault.


Resolution steps
   1. Assign the resource ID of the Azure key vault you intend to use with your wrap
     application to the variable.

   2. Confirm that the specified resource ID includes all required tags associated with the
     Bundle ID defined in the wrap wizard.

   3. Ensure you have permission to access your key vault:

      a. As a Microsoft Entra ID (formerly Azure AD) admin, add the service principal for the
        AppID "4e1f8dc5-5a42-45ce-a096-700fa485ba20" by running the following commands
        in PowerShell:

           PowerShell


           Connect-AzureAD -TenantId <your tenant ID>
           New-AzureADServicePrincipal -AppId 4e1f8dc5-5a42-45ce-a096-700fa485ba20 -
           DisplayName "Wrap KeyVault Access App"



      b. In the Azure portal   , under Access Control (IAM), assign the Reader role to your
        service principal:

         i. Go to Access control (IAM), and then select Add role assignment.
---

                                                                        


ii. Choose Reader under Job function roles and go to the Members tab.




                                                                        


iii. Search for your app name.




                                                                        


iv. Assign the Reader role.




                                                                        
---

For more information, see Step 2: Target platform.



Error code 1000132
Error message: Missing environment variable 'PA_Wrap_KV_ResourceID' for the targeted
environment.


Resolution steps
   1. Check whether the environment variable PA_Wrap_KV_ResourceID exists in the target
     environment. If it doesn't, create it.

   2. Ensure the name follows the correct naming convention without typos or formatting
     errors.

For more information, see Step 3: Choose target platform.



Other issues
If your issue isn't covered here, or if the preceding steps don't resolve your problem, search for
more support resources      or contact Microsoft support    and provide detailed steps to
reproduce the problem.



Related information
     "Something went wrong" error that occurs when using the wrap feature
     Troubleshoot common issues when using the wrap feature
---


## How to create a vanilla repro model-driven app

How to create a vanilla repro model-
driven app
Article • 04/02/2024


A vanilla repro app is a model-driven app that reproduces a problem in a vanilla
environment. Unlike canvas apps, model-driven apps in the same environment share
customizations like client scripts and server plug-ins. Therefore, it can be challenging to
determine whether a problem is caused by an incorrect customization or a product
issue.

Vanilla means no customizations. So a vanilla environment is an environment in its
original state, like a fresh installation. Using a vanilla environment with minimal
modifications to reproduce an issue can help rule out the possibility of a configuration
error.

After creating a vanilla repro app, you can share it with others, such as in the Microsoft
Power Apps Community        or through Microsoft Support      .



Create a vanilla environment
A vanilla environment doesn't refer to any specific type of environment in Power
Platform. You can create a new trial, sandbox, or developer environment to use as a
vanilla environment. But you need an appropriate license.

If you don't have a license to create new environments, consider simplifying the
customizations in your environment.



Recreate custom tables and other components
Microsoft Power Apps and Microsoft Dynamics 365 have some out-of-the-box tables
(entities) like Accounts and Contacts. To address issues with custom tables, you can
create similar ones in the vanilla environment. You don't have to copy the exact
configuration. For example, if the issue is with a column (field) of a table, create the
column for a new table.

The same principle applies to any customizations, such as business rules, commands,
forms, and views.



Create sample data
---

A vanilla environment initially has no data. For simple issues, you can manually add a
few rows (records). You can also add sample data for out-of-the-box tables.

If an issue requires specific data to reproduce, you can prepare a .csv or Excel file and
import data using the Power Platform admin center or import data into a model-driven
app.



Simplify developer customizations
Some advanced customizations require programming knowledge. These include client
scripts, code components (custom controls), classic commands, plug-ins, and web
resources. If they're necessary to reproduce an issue, simplify them as much as possible.
Remove any irrelevant lines of code and references to third-party libraries.



Isolate custom pages
Custom pages are a special type of canvas app. You can create a minimal repro canvas
app to demonstrate issues with custom pages. First, create a regular canvas app with
sample data. If the issue doesn't occur, it might be related to how the custom page is
integrated into the model-driven app. To further investigate, create a simplified version
of the custom page in a new model-driven app.



Export the vanilla repro app
After verifying that an issue exists in a vanilla environment, you can create an
unmanaged solution for the repro app.

It should include relevant customizations such as:

       A model-driven app (if it's not a standard Microsoft Dynamics 365 app like
       Customer Service Hub or Sales Hub.)
       Custom pages
       Dashboards
       Forms
       Relationships
       Tables
       Views

Then, you can export the vanilla repro app and any relevant customizations in an
unmanaged solution.
---

To verify whether the necessary components have been included, import the solution
into a different vanilla environment, and check if the issue can be reproduced.

Sometimes, other required materials can't be packaged into solutions. Here are some
other things to include with the vanilla repro app.


Sample data

Some issues require specific data to reproduce. As data isn't exported in a solution, you
need provide a .csv or Excel file with the necessary data. Remember to remove any
private and confidential data.


Source code
Advanced customizations created using JavaScript and C# can be difficult to package
into a solution, for example, classic commands or plug-ins.

It's easier to explain the problem by providing a copy of the source code and quoting
the relevant lines of code. Specify APIs that aren't working as expected.



Describe complex customizations
If the customizations are complicated, it can be difficult for others to understand, even if
they have a vanilla repro app. It's helpful to describe how these customizations are
made so that others can recreate them.



Why can't I reproduce an issue in a vanilla
environment
If an issue can't be reproduced in a vanilla environment, you need to check the
configuration. Some missing factors may not be accounted for in the vanilla
environment.

The fact that an issue doesn't occur in one environment is an important clue. By
systematically examining different types of customizations, you can figure out the
conditions that reproduce the problem.

Here are some reasons why a problem occurs in one environment but not in another:

     Customizations are interfering with normal operation. To confirm whether this is
     the case, add those customizations one by one to the vanilla environment or
---

     remove them from the environment where the problem occurs.
     Tables, relationships, and other components are configured differently. To
     confirm whether this is the case, reexamine the differences between the same
     components in the vanilla environment and the environment where the problem
     occurs.
     Components may be corrupted. To confirm whether this is the case, recreate them
     in the environment where the problem occurs.
     User-specific reasons. For example, some users have different security roles in one
     environment. To confirm whether this is the case, try alternative ways to access the
     data or perform the same task. Dataverse tables can be accessed in many ways,
     such as in model-driven apps, canvas apps, Power Apps table designer, Power
     Pages, and Web API requests.
     Different versions. The environment may be a different version or in a different
     geographical region. Check the About section in the app or environment details in
     the Power Platform admin center for version details.
     Issues with an environment's server. To confirm whether this is the case, examine
     network traffic to determine if the server is sending the correct information.
     Compare it with the network traffic in the vanilla environment.



Next steps
     Learn more about debugging strategies for model-driven apps
     Ask a question with the Power Apps community
     Get Microsoft Support



See also
     Debugging model-driven apps with Monitor




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Isolate issues in model-driven apps

Isolate issues in model-driven apps
Article • 04/12/2024


Model-driven apps are driven by configuration. You can give high-level instructions to
generate an app. You can also introduce custom components that affect multiple parts
of the app. When an app isn't behaving as expected, it may not be obvious if it's a
customization error or a bug in the Power Apps system.

Here are some techniques to isolate problems in a model-driven app.



Remove customizations
The following features can affect normal operation. Try disabling or removing them and
check if the problem still occurs. Learn more about finding and disabling customizations
on forms.


Business rules
Affects: Form pages

Business rules change a form's behavior based on the state of a record. Try disabling or
simplifying the rule and check if the form still works as expected.


Client scripts
Affects: Form pages

Client scripts contain JavaScript code that can conflict with the Power Apps system or
change it in unexpected ways. If disabling the script solves the issue, you should isolate
which part of the custom script causes the issue.

You can temporarily disable all custom scripts by appending this to the URL of the page:

  HTTP


  &flags=DisableFormLibraries=true,DisableWebResourceControls=true




Custom commands
Affects: Form pages, Table-based view pages
---

If a problem happens after selecting a command in the command bar, check if it's a
custom command. Custom commands can contain JavaScript code that causes
unexpected behavior. Modern commands can have custom actions defined with Power
Fx. In either case, try simplifying the command to find out if there's an error in how the
custom command is defined.


Custom controls
Affects: Form pages, Table-based view pages, Custom pages

You can replace controls on form pages or replace the grid control used on table-based
view pages with Power Apps components. These controls are custom controls with
JavaScript and CSS code that can affect other parts of the page. Try switching to an out-
of-the-box control to see if the custom control is the problem.


Server plugins and processes
Affects: All pages

Administrators can install plugins and create processes that modify the business logic of
an app. Check with your administrator if there are any relevant server-side
customizations.



Compare with out-of-the-box configurations
To help determine if something is a configuration error, it can be useful to check other
parts of the app.

For example, does the problem happen with a different:

     Table (entity)
     View
     App with the same table
     Form for the same table
     Control referencing the same column (attribute)

Ideally, compare with an out-of-the-box one that hasn't been customized. For example,
if the issue is with a table (entity) you created, check an out-of-the-box table.

If the problem doesn't happen elsewhere, compare the differences with how they're
configured. Perhaps table relationships and permissions are set up differently. Or a table
isn't enabled for Unified Interface.
---

Re-create items
Creating an item from scratch not only allows you to examine and compare default
configurations, it can also fix corrupted configurations.

If any of the following aren't working, try re-creating them. It can be a simplified version,
to narrow down which part isn't working.

     Custom table (entity)
     View
     Form
     Custom script



Ensure all required components are added to
an app
Model-driven app components include tables and their related tables, forms, columns,
views, charts, dashboards, and business process flows. For performance reasons, only
components added to an app will be downloaded.

If a component doesn't appear or behaves inconsistently, check if it's added to the app.
For example, if the Teams table doesn't appear in a form's lookup control, but other
tables do, then the Teams table might not have been added to the app.

You can add the following components to an app using the modern app designer.

     Tables and related tables: create a Dataverse table page
     Forms: add forms to an app
     Columns (form fields): add columns to a form
     Views and charts: manage views and charts on a Dataverse table page
     Dashboards: create a Dashboard page
     Business process flows: add a business process flow in the Automation pane

You can also add these components using the classic app designer.

For tables to be used offline, they have to be added to an offline profile. For more
information, see mobile offline guidelines.



Find out if the issue occurs when getting data
or showing data
---

When data isn't showing correctly in an app, it could either be a server issue in
providing the data, or an app issue in processing and displaying it. To narrow down the
cause, you can try general methods for isolating the problematic layer.

Model-driven apps have a complex data flow. Here are more advanced things to try.

     Examine the FetchXML of network requests and check if the app is making the
     right network requests and receiving data correctly from the server. You can use
     Monitor to view network requests.
     If the app has an offline profile, try removing the user from the profile or the
     profile entirely. Even when there's an Internet connection, the data flow is different
     for apps that can work offline.
     Check for permission issues by trying a different user or table.



Simplify custom scripts
Custom scripts are an advanced feature for developers. They can be used on forms,
custom commands, Power Apps components, and webpage (HTML) web resources.
There's enormous flexibility in what scripts can do, but there's also a high chance that
they can accidentally break the system.

If you suspect that a script is causing an issue, follow these steps:

   1. Disable all custom scripts and see if the issue still happens.

   2. If it doesn't, enable scripts one by one to see which one causes the issue.

   3. Once the script(s) are found that cause the issue, remove irrelevant code from
     them. For example, if only one field has a problem, remove code that interacts with
     other form fields.

   4. By progressively simplifying the script, you should be able to determine if the
     problem is caused by custom code or incorrect behavior of Client API features.

           If the error is from custom code, contact the developer who wrote the script
           for assistance.

           If a Client API feature isn't working as documented, you can report it to
           Microsoft. Attach a copy of the simplified script and mention which API
           feature isn't working.



Create a vanilla repro app
---

The process of creating a vanilla repro app may uncover configuration errors that aren't
obvious in an environment with many customizations. Even if the problem isn't fixed,
you would have narrowed the cause and made it easier to explain the problem to
others.



Next steps
     Troubleshoot commands
     Troubleshoot forms
     Troubleshoot plug-ins
     Troubleshoot permission issues with Microsoft Dataverse
     Debugging model-driven apps with Monitor
     Debugging model-driven apps forms with Monitor



See also
     General Power Apps debugging strategies




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot date and time issues in model-driven apps

Troubleshoot date and time issues in
model-driven apps
Article • 04/02/2024


When date and time values are off by a day or a few hours, it might be caused by time
zone or daylight saving adjustments. This article provides tips to troubleshoot issues
such as:

      The Date and Time field shows the wrong value.
      The Date only value shows the wrong date for some users and time zones.
      The Date and Time field shows the correct value in some parts of the app, but not
      others.
      After changing a date and time value and saving it, it changes automatically to a
      different value.
      Entering a daylight saving switchover date results in the date being off by one day
      or the time being off by an hour.



Determine if it's a server or client issue
Model-driven apps are web apps. They get data from the Dataverse cloud service
(server). The same data can power multiple apps (clients). Errors can occur on the server
or client.

If the date and time value stored on the server is unexpected, it will likely appear
incorrectly in all apps regardless of user or system time zone. Therefore, verifying the
server value is an important first step.


Check the configuration of the date and time column

Dataverse supports different time zone adjustment behaviors for date and time columns
(fields). Before troubleshooting, it's important to understand how different parts of the
system process date and time values.

Check the date and time column options in the Power Apps portal         or solution
explorer:

      Whether it accounts for a user's time zone
      Whether it displays the time part of the value
---

Check if the correct value is stored on the server
Date and time values are always stored as UTC on the server. You can view the raw value
on the server with a Web API query.

Here's a query to get a column for a row (record).

  HTTP


  [Organization URI]/api/data/v9.2/<entity set name>(<row id>)?$select=<column
  name>



The table and column names used are logical names, not display names.


   Tip

  An easy way to find the ID of a row is to open it in a model-driven app. The ID can
  be found in the page URL.


The following example gets the scheduledstart column of the appointment table for the
row with ID d2862246-4763-ee11-8def-000d3a34118b .

  HTTP


  https://myorg.crm.dynamics.com/api/data/v9.2/appointments(d2862246-4763-
  ee11-8def-000d3a34118b)?$select=scheduledstart



Entering this in the browser address bar will show something like the following:

  JSON


  {
      "@odata.context":
  "https://myorg.crm.dynamics.com/api/data/v9.2/$metadata#appointments(schedul
  edstart)/$entity",
      "@odata.etag": "W/\"11472725\"",
      "scheduledstart": "2023-10-15T07:30:00Z",
      "activityid": "d2862246-4763-ee11-8def-000d3a34118b"
  }



Therefore, the scheduledstart of the appointment is October 15th, 2023, 7:30 am. The Z
at the end indicates that the value is in UTC.

Let's say a user in the time zone UTC-8 views this column in a model-driven app. These
are the expected values for the different column options.
---

                                                                                ﾉ    Expand table


 Time zone adjustment behavior             Format               Value shown in the app

 User Local                                Date and time        October 14th, 2023, 11:30 pm

 User Local                                Date only            October 14th, 2023

 Time-Zone Independent                     Date and time        October 15th, 2023, 7:30 am

 Time-Zone Independent                     Date only            October 15th, 2023

 Date only                                 -                    October 15th, 2023


If the value shown in the app isn't adjusted correctly, it's likely a client issue. If the server
value is incorrect to begin with, it's likely a server issue.


Check the formatted value from the server
Time zone and daylight saving adjustments can be done on the server or in the app. If
the same column shows a different value in different parts of the app, it's likely that
some parts of the app are using the formatted value from the server, while others are
making the adjustments in the app.

This is likely an issue. Before reporting it, you can isolate whether it's a server or client
issue by checking the formatted value from the server.

For example,

  HTTP


  GET https://myorg.crm.dynamics.com/api/data/v9.2/appointments(d2862246-4763-
  ee11-8def-000d3a34118b)?$select=scheduledstart
  Accept: application/json
  OData-MaxVersion: 4.0
  OData-Version: 4.0
  Prefer: odata.include-
  annotations="OData.Community.Display.V1.FormattedValue"



The response will include the value adjusted by the server. In this example, the user is in
the UTC-8 time zone, and scheduledstart has User Local behavior. Therefore, the
formatted value is eight hours behind the raw value.

  JSON


  {
         "@odata.context":
---

  "https://myorg.crm.dynamics.com/api/data/v9.2/$metadata#appointments(schedul
  edstart)/$entity",
      "@odata.etag": "W/\"11472725\"",
      "scheduledstart@OData.Community.Display.V1.FormattedValue": "10/14/2023
  11:30 PM",
      "scheduledstart": "2023-10-15T07:30:00Z",
      "activityid": "2ad8786a-9164-ee11-9ae7-0022480a0700"
  }



If this formatted value is incorrect, it's a server issue. If it's correct, then it's a client issue.


Investigate unexpected server values

Possible reasons for unexpected server values are:

      You might not have configured the time zone adjustment behavior and format
      correctly.
      Business rules and workflows running on the server can change the value before or
      after it's saved. Inside an app, client scripts can change the value before sending it
      to the server for saving.



Determine if it's a customization issue or
product issue
Customizations can lead to unexpected behavior. The following methods can help rule
out problems caused by customizations.



Disable custom scripts
Custom scripts frequently cause issues. Try disabling them temporarily.



Create a new date and time column
Creating a new date and time column is the easiest way to find out if the issue is caused
by configuration errors or customizations like business rules. Ideally, use a different
table and app.

If the new column works as expected, it's likely a customization issue. Compare with the
original column to find the difference.

If the new column has the same problem, it might be a product issue. You can create a
vanilla repro model-driven app and report it through a support request.
---

Try a different time zone
To find out if time zone and daylight saving adjustments are causing unexpected values,
try changing the user's time zone.

There are two settings that affect time zones in model-driven apps:

   1. Time zone in personal options.
   2. System time zone. For information on how to change it, see the respective
     documentation in Windows, Android, iOS, or macOS.

Useful combinations to try:

     Match the time zone in personal options with the system time zone.
     Use UTC time zone.
     Use a time zone with the same offset, but doesn't observe daylight saving.


   Tip

  The following methods provide more details to make it easier to investigate date
  and time issues.

        Change the "Date Only" format to "Date and Time"
        Don't use 2-digit years




Change the "Date Only" format to "Date and
Time"
If a date-only value is off by a day, it's helpful to show the time part to see if time zone
adjustments could be the cause. You can temporarily change the column format in the
Power Apps portal     or solution explorer.



Don't use 2-digit years
The 2-digit year is ambiguous. For example, 40 might mean 1940, 2040, or 2140. How
the system interprets 2-digit years can and will likely change over time.

It's also difficult to investigate when the complete date and time values aren't shown.
For these reasons, it's strongly recommended to use 4-digit years, especially when
entering dates.
---

If you can't switch to 4-digit years permanently, try it temporarily to help troubleshoot.



See also
Behavior and format of the Date and Time column




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot Lookup control issues in

Troubleshoot Lookup control issues in
model-driven apps

Summary
This article explains how to troubleshoot lookup control issues in Power Apps model-driven apps.
The Simple and Advanced Lookup controls use the Lookup field, its relationships, the assigned
view, the entity's Quick Find view, the search string, and any applied custom script to build a
FetchXML for retrieving search results.

Issues with this operation usually fall into one of these categories:

     Search results are incorrect.
     Views are incorrect.
     Result fields are incorrect.


Search results are incorrect
If the Lookup control's search results are missing items or include unexpected items, inspect the
FetchXML of the outgoing network request that the control makes.

     If the FetchXML is incorrect, the problem is that:

        The Quick Find view or the view being searched is misconfigured:
           Missing search fields.
           Missing the primary field.
           Using a filter that blocks results.

        A client script modifies the control's behavior by using APIs such as addPreSearch or
        addCustomFilter.

     If the FetchXML is correct, but the data returned is incorrect, the issue is on the server, such
     as a misconfigured relationship. Another possibility is that the user doesn't have correct
     permissions for some entities, which might not be apparent in the network response other
     than by an omission of results.


   Tip
---

  Search results are listed in the order they're returned from the server. If results aren't in the
  expected order, then either

        the FetchXML order element has the wrong attribute values, or
        the server is unable to sort the results, such as with virtual entities.



  ７ Note

        Selecting the text area (the input box of the Lookup control) shows a list of the most
        recently used items, not a fresh search.
        Selecting the magnifying glass triggers a search based on your input, showing results
        that match your search terms. You can configure the control to always perform a search
        when you select the text area, instead of showing recent items.



Views are incorrect
     If an entity or view is missing from the Lookup control's views or results, or the default view
     is incorrect:
        Verify that the entity is enabled for the app.
        Verify that you have the permissions and roles required to interact with the entity and
        related entities.

     If the addCustomView API is being applied, verify that the viewId isn't already used.

     If the lookupObjects or setDefaultView API is being applied, verify that the viewId belongs
     to a view that's included in the current app.


Result fields are incorrect
The Simple Lookup control presents the search result fields in the order that they're listed in the
entity's Lookup view, with the following exceptions:

     Blank fields are replaced with the next nonblank field.
     Fields beginning with the search string are swapped with the second field.


  ７ Note
---

 A multi-entity Lookup control can have results with different orders of fields if the entities'
 Lookup views have different field combinations.



See also
     General Power Apps troubleshooting strategies
     Isolate issues in model-driven apps - Power Apps
     Records aren't filtered in lookup for particular entity
     Work with Quick Find's search item limit (Microsoft Dataverse)



Last updated on 05/29/2026
---

Lookup doesn't filter records as
expected for particular entity in
Dynamics 365
Article • 11/30/2022


This article provides workarounds to an issue in which the lookup displays all records
instead of only the records that are related to what you typed in.

Applies to: Power Apps
Original KB number: 4603850



Symptoms
When you type into a lookup control, the lookup displays all the records in the view
instead of only the records that are related to what you typed in. If you scroll through
the records, you see record text bolded like normal when the text matches the search
text.




Cause
There are two potential causes of this issue:
---

Cause 1
The issue occurs because there are no "find" columns in the Quick Find View of the
entity.

The Lookup view determines what columns are displayed inside of the lookup control,
but the Quick Find View - Find columns determines what columns are searched inside
the lookup control. Basically, when you type a value into a lookup control, it searches for
a match inside of the find columns. It then selects records with a match, and displays
information determined by the Lookup view to you. The reason why it shows all records
is that there are no "find" columns set in the Quick Find View.


  ７ Note

  Quick Find View columns are not the same as Quick Find View - Find columns.
  There can be many columns inside the Quick Find View, but if none are marked as
  "find" columns, the search will not work as expected.


The reason why the displayed and searched columns can be different is their
performance. The fewer columns searched, the faster the search can be executed.
However, you might want to see lots of information in the lookup control to make sure
you select the right record.

For the steps to add "find" columns, see Workaround 1.


Cause 2
The issue occurs because there are no string type columns in the view being used by the
lookup control.

The lookup control can't filter non-string type columns. The view being used needs to
have at least one string type column, such as text, email, phone, url, and so on.

For the steps to add a string type column, see Workaround 2.



Workarounds
To work around this issue, use one of the following workarounds:


Workaround 1
---

   1. In Customizations, go to the Quick Find View for the entity of the lookup control.

   2. Select Add Find Columns.




   3. Add any columns that you want to be searched and matched inside of the lookup
     control.




   4. Save and publish changes.


Workaround 2
You need to add a string type column to the view used by the lookup control.
---

   1. In Customizations, go to the view used by the lookup control where filtering is
     broken.

   2. Select Add Columns.




   3. Add at least one string type column.




Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

"Refresh All" doesn't work after
exporting app data to a dynamic
worksheet
Article • 10/25/2023




Symptoms
You use the Export to Excel command to export app data to a dynamic worksheet. Then,
you open the downloaded file and refresh the data by selecting Data > Refresh All. In
this situation, you find that the data disappears and the workbook appears blank. You
might receive the following error message:

  This Web query returned no data. To change the query, click OK, click the arrow on
  the name box in the formula bar, click the name of the external data range for the
  Web query, right-click the selection, and then click Edit Query.



                                                                                  



Cause
This issue occurs when the data that you access is password-protected and the Excel file
can't submit passwords to external data sources.



Resolution
To resolve this issue, you must edit and save the web query.

   1. In the Excel file, select Data > Queries & Connections.
---

2. The Queries & Connections pane opens on the right of the window. On the
  Connections tab, right-click the query and then select Properties.




3. The Connection Properties window opens. On the Definition tab, select Edit
  Query.
---

4. If prompted, enter the username and password. Enter the same user and password
  that you use to sign in to your app.

5. On the Edit Web Query window, select Go. An error message occurs:

    Can't complete this action




                                                                            


6. Close the Edit Web Query window.
---

   7. This should fix the issue. Refresh the data in the worksheet again by selecting Data
     > Refresh All.




If the above steps don't resolve the issue, follow these additional steps:

   1. Enter the following link in the address bar of the Edit Web Query window to
     access the Advanced Settings page in Microsoft Dynamics 365 Customer
     Engagement. Remember to replace OrgURL with your organization URL.

      https://OrgURL/main.aspx?settingsonly=true


   2. Sign out using the top-right profile option link and then sign back in using the
     right identity.

   3. Once you're signed in, close the Edit Web Query window, and then in the Excel
     file, select Data > Refresh All. The data will be refreshed as expected.



See also
Export data to an Excel dynamic worksheet




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot view issues in model

Troubleshoot view issues in model-
driven apps
Article • 04/02/2024


Model-driven apps use views to define how a list of records for a specific table is
displayed in the application.

A view defines:

      The columns to display.
      The order of the columns.
      The width of each column.
      The default sorting of record lists.
      The default filters applied to restrict the records displayed.

Once a view is available in the app, users can select it.

This article describes some of the most common issues related to views and suggestions
to resolve them.

      View selector renders incorrectly.
      Public view isn't shown in the view selector.
      View selector is blank after navigating from a dashboard.
      Personal views aren't shown in the view selector.
      Column doesn't appear in the column editor's "Add columns" list.
      Shared personal views are missing from the view selector.
      The "Save changes to current view" option is missing.



View selector renders incorrectly
If the view selector isn't rendering correctly, check if there's a third-party CSS library on
the form. Because the library's styles operate on the global style (that is, there's no
namespace), these styles affect all elements on the page. Our CRM controls, including
the view selector, weren't designed for libraries like Bootstrap, thus often causing these
issues. If you're using Bootstrap or similar CSS libraries, consider removing them.



Public view isn't shown in the view selector
If a public view isn't shown in the view selector, check the app designer to verify that the
view is included in the app. If it isn't included in the app, use the app designer to add
---

the missing view to the app.



View selector is blank after navigating from a
dashboard
If the view selector is blank when you navigate to any entity from a dashboard using
"see all records," this might mean that the view used on the dashboard isn't included in
the model-driven app. To solve this issue, add the missing view to the app.



Personal views aren't shown in the view
selector
If you don't see personal views in the grid selector, it might be because when a subgrid
on a form is configured to show all views, it renders the My Views selections. This
configuration conflicts with the homepage grid view (sample UI):




To fix this issue, you can modify the default entity form so that all subgrids don't use
Show All Views.

The following screenshot shows an example case form containing a subgrid with Show
All Views enabled:
---

                                                                                  


If the subgrid configuration is changed to Off or Show Selected Views, as shown in the
following screenshots, the issue with the missing views should no longer occur.
---

Column doesn't appear in the column editor's
"Add columns" list
Sometimes, you might expect a specific column to appear in the column editor's Add
columns list, but you can't find it.
---

This issue usually happens because the isValidForGrid attribute is set to false. You can
get the metadata for the attribute by adding the following path to the organization URL
(replacing account and address1_longitude with the desired entity and attribute name):

/api/data/v9.2/EntityDefinitions(LogicalName='account')/Attributes(LogicalName='add

ress1_longitude')?$select=SchemaName,IsValidForGrid


If isValidForGrid is set to false, this attribute can't show up in the grid and, therefore,
doesn't show up in the column editor. To solve this issue, set IsValidForGrid to true.



Shared personal views are missing from the
view selector
---

Some users might not see personal views shared with them in the view selector, even
though they appear in the Manage and share views dialog.

This behavior might be because the users don't have the "Direct User (Basic)" access to
the "Saved Views" entity. The access provided by an owner team that has the "Team
privileges only" inheritance setting isn't sufficient.

To solve this issue, provide the impacted users with the "Direct User (Basic)" access to
the "Saved View" entity instead of the "Team privileges only" access.




The "Save changes to current view" option is
missing
The Save changes to current view option only appears in the command bar when
modern advanced find is turned off; otherwise, it only appears in the view selector.




Furthermore, this option is only shown for personal views. When you select a system
view using All Accounts > My Active Contacts, the option isn't shown, as a system view
can't be updated. This behavior is by design.



See also
     General Power Apps troubleshooting strategies
---

     Isolate issues in model-driven apps - Power Apps
     Understand model-driven app views
     FAQ for grid views

Third-party information disclaimer

The third-party products that this article discusses are manufactured by companies that
are independent of Microsoft. Microsoft makes no warranty, implied or otherwise, about
the performance or reliability of these products.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshooting grid issues in Power

Troubleshooting grid issues in Power
Apps
Article • 10/10/2024


This guide helps you resolve the following grid issues that occur in a Power Apps
model-driven app.

      Can't use sorting or sorting doesn't work correctly.
      Can't use column filters on a grid or subgrid or filtering doesn't work correctly.
      Can't edit data in the grid after enabling editing mode.
      Grid or subgrid displays incorrect content.
      Grid or subgrid doesn't display all the records.
      Grid filter for a lookup column doesn't show any suggestions.
      Modern Advanced Find doesn't work correctly.
      Nested grid doesn't display data.
      Quick Find doesn't return correct results.
      Some columns don't contain data.
      The overall record count doesn't match the displayed content.



Terms
   1. Grid control - a control that's displayed on an entity page.
   2. Subgrid control - a control that's displayed in a form or inside a reference panel.
   3. View selector - a drop-down control that allows selecting the current view.
   4. Ribbon command bar - the content-dependent button bar at the top of a page or
      form.
   5. Subgrid menu - a content-dependent menu.
   6. Quick Find - a search control that allows filtering the current view by typing a
      search string.
   7. Column Editor - a tool that allows adding, removing, or reordering columns in the
      current view.
   8. Modern Advanced Find - a tool that allows applying complex filters to the current
      view.
   9. Column filters - a tool that allows applying simple filters to the grid.
  10. Column sorting - a tool that allows sorting the grid content by one or more
      columns.
  11. Status column - a grid column that allows selecting rows. It's also used for
      displaying row related messages.
  12. Nested grid - a child grid that renders inside a grid or subgrid control.
---

 13. Column header - the header at the top of the grid or subgrid control.
 14. Jump bar - the alpha-numeric bar at the bottom of the grid.

Here are the screenshots of the terms:




                                                                             




                                                                             




                                                                             
---

                                                                                     



Useful tools
   Power Apps Monitor tool
   Web Developer tool



Steps to perform before starting
troubleshooting
 1. Remove or disable custom scripts. One of the first steps is to ensure that custom
   scripts don't interfere with product functionality. It's highly recommended to
   perform this step even when custom scripts are used to work in one of the
   previous versions.

        If all custom scripts are attached via form events, follow the steps in
        Troubleshoot form issues in model-driven apps to disable them.
        Other custom scripts are added directly via web resources, custom solutions,
        or plugins.
        If the issue can't be reproduced after removing custom scripts, investigate all
        the customizations to find the problem.
        If custom scripts are correctly using publicly documented APIs and the
        product doesn't behave as expected, try to simplify the custom script to
        localize the problem. In most of the cases, 10-30 lines of script code are
        enough to reproduce an issue.

 2. If the problem involves custom entities, custom relationships, custom views,
   custom configurations, or other custom resources, try to reproduce the issue with
---

     out-of-the-box (OOB) standard resources and avoid any custom resources. This
     method helps localize the problem.

   3. Disable all the applicable business rules to see if the issue is caused by a business
     rule.

   4. If reproducing the issue involves the use of third-party tools, try to reproduce the
     issue with standard OOB tools.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Can't use sorting or sorting doesn't
work correctly in a Power Apps model-
driven app
Article • 08/16/2024


This article helps solve an issue where you can't use sorting or sorting doesn't work
correctly in a model-driven app in Microsoft Power Apps.



Scenario 1: None of the columns are sortable in
the grid

Resolution
Sorting not available on all the columns is a strong indication that sorting is disabled on
the grid control. Use the Power Apps Monitor tool to make sure the enableSorting grid
property is set to true .
---

                                                                       


If sorting isn't enabled, update the respective grid property value.
---

Scenario 2: Sorting doesn't seem to be correct
after navigating to the grid or subgrid

Resolution
If there's no custom code that alters the sorting, the default sorting should correspond
to the Sort by setting in the current view.




                                                                                    


Make sure the view setting is set correctly and all the changes are saved and published.



Scenario 3: Certain columns aren't sortable in
grid. Respective column header menu options
are missing or disabled

Resolution
The most common reason why a certain field isn't sortable is that Dataverse doesn't
support sorting on the underlying field type. Use the Power Apps tool to ensure the
sorting isn't disabled by Dataverse.
---

                                                                                        


If sorting is disabled ( "disableSorting": true ), this is a strong indication that the sorting
isn't permitted on the data field (column). For more information about sortable columns,
see Types of columns.



Scenario 4: Column is sortable but the data
isn't ordered correctly

Troubleshooting step
   1. Ensure the column is in the expected format (see the dataType and Format
     attributes in the image of scenario 3).


        ７ Note

        Data sorting is always performed based on the column type and format rather
        than the actual data. For example, sorting is always "alphabetical" on text type
        columns, even if all the data in these fields is numeric.


   2. Check if the data is sorted (ordered) by more than one column. The presence of
     sorting icons on more than one column indicates multi-column sorting. In this
---

     case, the data sorting is performed on the first sorted column (which is not
     necessarily the leftmost column) and then on the second column. As shown in the
     following example, the data is sorted first by the Full Name column ascending and
     then by the Company Name column descending.




                                                                                      


     The multi-column sorting can be removed by reapplying the sorting on a column
     (without holding the Shift key down) or by refreshing the app.

   3. The data ordering might be affected by data customizers.


        ７ Note

        Sorting (data ordering) is always applied to raw data, not enhanced data. A
        typical example is the case where raw numeric data is replaced by a user-
        friendly text, in which case the ordering is performed by the numeric data.




See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Can't use column filters on a grid or
subgrid or filtering doesn't work
correctly in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for different scenarios where you can't use
column filters on a grid or subgrid, or filtering doesn't work correctly in a Power Apps
model-driven app.



Scenario 1: Column filtering isn't enabled on
any of the columns

Troubleshooting step
Make sure the enableFiltering grid property is set to true . If it's set to false , check
the grid control configuration to make sure the respective Enable Filtering property is
enabled.
---

                                   



Scenario 2: Column filtering options are
missing or disabled on certain columns
---

Troubleshooting step
After checking to ensure there's no custom code that affects filtering, use the Power
Apps Monitor tool to check the column type.


  ７ Note

  Dataverse doesn't support filtering on certain columns. For more information about
  searchable columns, see Types of columns. Here's an example of a property type
  that doesn't support filtering:
---

                         




Scenario 3: Column filtering is enabled but not
applied correctly

Troubleshooting step
---

The most common cause is that extra filters are applied to the current view. Use the
Power Apps Monitor tool to inspect the fetchXML query (see Image 6) and check all the
filters that are shown in the query.




Additionally, other filters can be found in:

     A quick find search.

     A jump bar filter.




                                                                                   


     Relationships with the parent entity.
---

An entity specific filter (for example, a queue or an activity).




A grid-related filter.

You can use the Power Apps Monitor tool to inspect grid-related filters (see the
following screenshots) and compare them with the final fetchXML query.
---

In the following screenshots, a grid column filter with a name like %Coffee% or a
name containing Coffee is used.




                                                                              
---

See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Can't edit data in the grid after enabling
editing mode in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for different scenarios where you can't edit
data in the grid after enabling editing mode in a model-driven app in Microsoft Power
Apps.



Scenario 1: The entire grid control isn't editable
even though editing mode is enabled

Troubleshooting step
The first step is to check the grid and column parameters using the Power Apps Monitor
tool.
---

                                                                                    


Make sure the grid editable mode is set to yes . If not, check the grid configuration and
make sure the last configuration is saved and published. Also note that the form might
also forcibly set sub-grids to read-only or disabled modes in certain cases (for example,
when the currently edited record is deactivated). You can troubleshoot this issue by
checking the isControlDisabled attribute.
---

Scenario 2: Only certain cells from certain
columns aren't editable

Troubleshooting step
Use the Power Apps Monitor tool to check the attributes of the column that isn't
editable (see the first screenshot in this article). If the IsEditable attribute is set to
false , then editing isn't allowed here. Possible reasons include but aren't limited to:


     Dataverse doesn't support editing of the underlying column type. For example,
     calculated type columns aren't editable.
     The user might not have permission to edit that column.
     A custom script alters the cell attribute, making it permanently or conditionally
     read-only.



See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Grid or subgrid displays incorrect
content in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for an issue where the grid or subgrid
displays incorrect content in a model-driven app in Microsoft Power Apps.



Symptoms
You might find the grid doesn't display the expected content immediately after
navigating to the parent page or form. Data is rendered but the content doesn't match
the default view or the view selected from the view selector.



Troubleshooting step
The first step is to check if the grid receives the expected data. Use the Power Apps
Monitor tool to investigate the latest "GridChecker" event that's related to the grid or
subgrid.




                                                                                       


If the recordsCount and initialPageSize matches the actual content displayed in the
grid, this is a strong indication that the view isn't configured correctly. Check the view
configuration (columns and filters). If the issue occurs in a subgrid, also check if the grid
is configured to only show related records.



More information
---

     For similar issues, see Grid or subgrid doesn't display all the records and The
     overall record count doesn't match the displayed content.
     For other grid issues, see Troubleshooting grid issues in Power Apps.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Grid or subgrid doesn't display all the
records in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for an issue where you might find the
content displayed in the grid or subgrid in a Power Apps model-driven app is correct,
but it seems incomplete.



Troubleshooting step
      For a grid control, make sure the page size and the number of records provided to
      the grid control are expected.




                                                                                    


      For a subgrid, the page size can be also defined by the Maximum number of rows
      setting (a subgrid component) in the form designer.
---

More information
     For similar issues, see Grid or subgrid displays incorrect content in a model-driven
     app and The overall record count doesn't match the displayed content.
     For other grid issues, see Troubleshooting grid issues in Power Apps.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Grid filter for a lookup column shows no
suggestions in a model-driven app
Article • 10/10/2024



Symptoms
When you try to filter data on a lookup column, you don't see a list of values, or the
filter results box says "No Records Found." For example, the filter on the Parent Business
column doesn't show any results, as shown in the following screenshot.




Cause 1
The records for this lookup field don't have their primary field populated. Therefore, the
filter list is blank.


Resolution
The records have to populate their primary field.
---

Cause 2
The Lookup View for the entity that's associated with the column doesn't add the
primary field as part of its view, as shown in the following screenshot.




                                                                                   



Resolution
Edit the Lookup View for the entity and add the primary field.
---

                                            



More information
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Modern Advanced Find doesn't work
correctly in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for issues where the Modern Advanced Find
feature doesn't work correctly in a model-driven app in Microsoft Power Apps.



Scenario 1: Some filter conditions reappear
after being deleted

Troubleshooting step
Check if the automatically reapplied filters are related to the page filters. Some entities
(activities and queues) support the page filters (see the following screenshot). Those
filters can't be removed from the Modern Advanced Find window.




Scenario 2: Some filter conditions aren't
rendered correctly

Troubleshooting step
Modern Advanced Find currently doesn't support the following conditions:
---

   The Date type fields used with standard operators. The Date type fields must be
   used with field-specific operators. For example, on should be eq , and on-or-
   before should be lt .

   The in type conditions. To ensure compatibility with Modern Advanced Find, the
   in type conditions should be replaced with several eq . For example, [city in

   "Redmond", "Washington" ] should be replaced with [city eq "Redmond" Or city
   eq "Washington"] .




Scenario 3: Unexpected data after applying
Modern Advanced Find filters

Troubleshooting step
 1. Use the Power Apps Monitor tool to obtain the fetchXML query and the
   recordsCount attribute.
---

                                                                                      


   2. Check all the filters in the fetchXML query and make sure they're all expected.




     If the fetchXML query contains extra filters, check for any extra filters that might be
     applied. For more information, see Scenario 3: Column filtering is enabled but not
     applied correctly.



See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?     Yes    No
---

Provide product feedback
---

A nested grid doesn't display data in a
Power Apps model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for an issue where a nested grid doesn't
display any data in a Power Apps model-driven app.



Cause
The most common reason is using an incorrect relationship or applying an incorrect
view.



Troubleshooting checklist
   1. Make sure the nested grid is configured with the correct relationship.

        The Child Items Parent Id parameter must be set to a lookup type field from the
        entity assigned to the parent grid (bound to Accounts entity as shown in the
        following screenshot). The lookup field should point to the nested grid entity.
        Make sure it's a standard lookup type with a standard N:1 (many-to-one)
        relationship.




   2. Check if the view assigned to the nested grid (the My Active Accounts in step 1)
        contains any unexpected filters.

   3. Use the Power Apps Monitor tool to inspect the data for the nested grid.
---

                                                                                



７ Note

The childRecordsCount attribute should display the number of records in the
nested dataset. If that attribute shows 0 , it's a strong indication of an
incorrect relationship specified, the presence of extra filters in the nested grid
view, or no records in the nested dataset ( ChildItems ). If that number shows a
value greater than zero, and your nested grid still doesn't display any records,
the issue is most likely with the extra filtering in the nested grid view or there
being no records related to the row expanded from the parent grid. Check the
childViewFetchXML and ChildViewFields and make sure all the filters are
---

        correct and that all the column definitions match those specified in the
        childViewFetchXML .




See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Quick Find doesn't return correct results
in a model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for an issue where a quick find search doesn't
return correct results in a Power Apps model-driven app.



Troubleshooting checklist
   1. Use the Power Apps Monitor tool to inspect the fetchXML query that is generated
      based on a quick find search.




   2. Check the recordsCount attribute in the fetchXML query.
---

                                                                                     


 3. The Quick Find filter is marked with the isquickfindfields attribute.




                                                                                     


   If the columns from the isquickfindfields filters are incorrect, it's a strong
   indication that your organization's Use quick find view of an entity for searching on
   grids and sub-grids setting isn't set correctly.

        If the setting is turned off, the search will be performed on all the searchable
        columns. For more information, see Types of columns.
        If the setting is enabled, the search will be performed based on the entity's
        quick find view. Also, note that the entity's quick find view might contain a
        filter that will be applied to the search. You should be able to see that filter in
        the fetchXML data query that you inspect.



More information
---

     About quick find queries
     Best Practices for Dynamics 365 CRM Quick Find View
     Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

Some columns don't contain data in a
model-driven app
Article • 08/16/2024


This article provides troubleshooting steps for an issue where some columns don't
contain data in a model-driven app in Microsoft Power Apps.



Symptoms
You might find data isn't displayed in certain columns in a Power Apps model-driven
app.



Cause
This issue is often caused by the discrepancies between the fetchXML request (the query
for data) and the layoutXML (the column definitions), which might be due to custom
code that incorrectly modifies the query. Before troubleshooting the issue, follow the
steps described in Steps to perform before starting troubleshooting.



Troubleshooting step
First, you should ensure the issue isn't related to insufficient permissions. The easiest
way to check this is to navigate to the page as a user with full administrative privileges.
The Power Apps Monitor tool can also be used to ensure the column data is readable.
---

                                                                                      


If the issue isn't related to insufficient permissions, use the Power Apps Monitor tool to
check the query and columns definition as shown in the following screenshot.
---

                                                                                     


Make sure that all the columns listed in the viewFields section are present in the
viewFetchXML query and that the respective columns aren't marked as hidden .


The issue can also be caused by a corrupt view. Resaving and republishing such a view
might help solve the problem.



See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

The overall record count doesn't match
the displayed content in a model-driven
app
Article • 08/16/2024


This article provides troubleshooting methods for an issue where the overall record
count doesn't match the displayed content in a Power Apps model-driven app.



Symptoms
A typical example of this issue is that the number of records displayed is lower than the
count displayed at the bottom of the page.



Cause
The most likely reason is that the data displayed in the grid contains duplicate records
(by the value in the primary field). The issue is caused by pulling related record
duplicates from the same table.



Troubleshooting checklist
      Use the Power Apps Monitor tool to check the total number of records.




                                                                                        


      If the recordsCount matches the total number of records displayed at the bottom
      of the grid, but the data in the grid has fewer records, it's a strong indication that
---

the data contains duplicate records. Use the monitoring tool to get the current
viewFetchXML request.




                                                                             


The issue can be solved by adding distinct="true" to the fetchXML query. For
more information, see Query data using FetchXml.

If adding distinct="true" doesn't solve the problem, consider changing the query
to avoid pulling duplicate records. The primary column (field) can also be found by
using the Power Apps Monitor tool.
---

See also
Troubleshooting grid issues in Power Apps




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshooting ribbon issues in Power

Troubleshooting ribbon issues in Power
Apps
Article • 09/25/2023


This guide helps you resolve issues that affect a ribbon command bar button in a Power
Apps model-driven app or a customer engagement app (Dynamics 365 Sales, Customer
Service, Field Service, or Marketing).

Applies to: Power Apps
Original KB number: 4552163



Use Command checker
Command checker is a tool for examining command (ribbon) definitions and
troubleshooting common issues. It's built into every Power Apps model-driven app and
Dynamics 365 app.


  ７ Note

  Command checker only works in a web browser. We're adding support to Android
  and iOS apps soon. As a workaround, check if the same issue occurs when the app
  is opened in an Android or iOS browser. If it does, you can use Command checker
  to investigate.


Use Command checker to diagnose common issues like:

      A button on the command bar is hidden when it should be visible
      A button on the command bar is visible when it should be hidden
      A button on the command bar isn't working correctly
      A button on the command bar has wrong labels


  ） Important

  These issues are often caused by missing or incorrect ribbon metadata. Typically,
  this situation can be resolved by regenerating all ribbon metadata. Command
  checker has a feature that enables you to trigger the regeneration of all ribbon
  metadata. Only system administrators, system customizers, and makers have the
  permissions to regenerate metadata.
---

Enable Command checker
To enable Command checker, append the &ribbondebug=true parameter to the URL of
the app. For example: https://yourorgname.crm.dynamics.com/main.aspx?appid=
<ID>&ribbondebug=true .




                                                                                



Inspect a command
Once Command checker is enabled, you'll find a new button named Command Checker
    in various command bars (global, main form, main grid, and subgrid). You may have
to expand the menu bar to see this button.


  ７ Note

  Command checker isn't available for commands in Quick actions.


   1. Find the command bar that has the command you want to investigate.
   2. Select the Command Checker button. The Command checker panel opens.
   3. Select the command you want to examine in the list of commands. Commands
     that aren't visible are displayed in italics and end with (hidden).



Reference
Command checker for model-driven app ribbons




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

A button on the command bar is hidden
when it should be visible in Power Apps
08/11/2025


Applies to: Power Apps
Original KB number: 4552163



Determine why a button is hidden
A button can be hidden due to an enable rule or display rule on the command associated with
the button evaluating to false. It could be that the associated command has a
Mscrm.HideOnModern display rule that would hide the button in Unified Interface applications. A

HideCustomAction could also have been created that would force the button to be hidden. If
the user is offline, custom commands and default commands without the
Mscrm.IsEntityAvailableForUserInMocaOffline enable rule won't be displayed.



  ２ Warning

       Any display rule of the EntityPrivilegeRule type with a PrivilegeType value of one of
       the following (Create, Write, Delete, Assign, Share) will evaluate to false if the entity
       has the Read-Only in Mobile option enabled, which will force the entity to only
       permit Read privilege. Examples of some of the most common default system rules
       that will evaluate to false when the Read-Only in Mobile flag is enabled on the
       entity, are as follows, but not limited only to this list
       ( Mscrm.CreateSelectedEntityPermission , Mscrm.CanSavePrimary ,
        Mscrm.CanWritePrimary , Mscrm.CanWriteSelected ,

        Mscrm.WritePrimaryEntityPermission , Mscrm.WriteSelectedEntityPermission ,

        Mscrm.CanDeletePrimary , Mscrm.DeletePrimaryEntityPermission ,

        Mscrm.DeleteSelectedEntityPermission , Mscrm.AssignSelectedEntityPermission ,

        Mscrm.SharePrimaryPermission , Mscrm.ShareSelectedEntityPermission ). You can edit

       the entity and uncheck the Read-Only in Mobile option to permit these rules to
       evaluate to true, provided the privilege being tested by the rule is also granted to
       the user.
       Do not remove the Mscrm.HideOnModern display rule from a command to force a
       button to appear in the Unified Interface. Commands that have the
---

     Mscrm.HideOnModern display rule are intended for the legacy Web Client interface and

    are not supported in the Unified Interface, and might not work correctly.


1. Enable Command checker and select the command button to inspect.

2. The following example shows the New button on the contact entity's grid page isn't
  visible and is represented by an item labeled New (hidden).


    ７ Note

    If your button doesn't appear in the list, it might be hidden for one of the following
    reasons:

     a. HideCustomAction customization:

               In the left navigation panel, look for the HideCustomAction section at the top.
               Expand the list and review each item. Check the location properties for a
               match with your button's name.
               If a match is found, this is likely why your button is hidden. To resolve the
               issue, follow the Repair Options instructions, but apply them to the
               HideCustomAction instead of a command.


     b. Mscrm.HideOnModern display rule:

               The associated command might have a Mscrm.HideOnModern display rule,
               which hides the button in Unified Interface applications.
               Currently, the Command Checker tool doesn't list buttons hidden by this
               rule. This limitation is being addressed in a future update.

     c. Manually hidden in the command bar designer:

               Open the command bar designer for your app.
               Locate your button and check the properties pane.
               At the bottom, verify that the Hidden field isn't checked.
---

    ７ Note

    If the button remains hidden even when all rules evaluate to True, check the hidden
    reason in the navigation panel:

          Hidden by selection:
               It means that the button is hidden due to context sensitive commands in
               grids.
               When records are selected in a grid, any button without a
               SelectionCountRule element is considered not relevant to the selected

               record(s) and will be hidden, even if its rule evaluation is True.
               Note that flyouts aren't affected, as flyout children might still have record-
               based commands.

          Hidden offline:
               The command is hidden because you are offline, or the app is set to offline
               by default.
               This command isn't supported in offline mode. You can adjust your app's
               offline settings and disable offline-first if needed.


3. Select the Command Properties tab to display the details of the command for this
  button. This will show the enable rules and display rules, along with the result (True, False,
  Skipped) of each rule evaluation. The following example shows the New (hidden)
  button's command to be Mscrm.NewRecordFromGrid and there's an enable rule named
  new.contact.EnableRule.EntityRule that has evaluated to False, as a result the button will

  be hidden.
---

4. Expand the new.contact.EnableRule.EntityRule enable rule, by selecting on the chevron
     icon to view the details of the rule. To understand why a rule evaluates to True or False
  requires a little understanding of the type of rule. For details of each type of rule, see
  Define ribbon enable rules, and Define ribbon display rules. The following example shows
  that the rule type is Entity and the entity logical name is account. Since the current entity
  is contact, which isn't equal to account, this rule returns False.
---

 5. The approach needed to fix a button's visibility will depend on the various customizations
   in your specific scenario. Considering our example:

        If this rule was created erroneously, such that the entity declared in the rule was
        intended to be contact but was set to account, you could edit the
         new.contact.EnableRule.EntityRule enable rule and make changes that would

        permit the rule to evaluate to true.
        If this rule was added to the command unintentionally, you could modify the
         Mscrm.NewRecordFromGrid command and remove the
         new.contact.EnableRule.EntityRule enable rule from the command definition.

        If the command is an override of a Microsoft published definition, then this custom
        version of the command could be deleted to restore the default functionality.



Repair Options
---

Select a repair option from one of the tabs below. The first tab is selected by default.


  Delete the command




  How to delete a command

  If there's another solution layer that contains a working definition of the command, then
  you can delete the definition to restore the inactive working definition.

  If this is the only layer and you no longer need the command, then you can remove it from
  your solution if no other button is referencing the command.

  In order to delete a command, we need to determine which solution installed the
  customization:

     1. Select the View command definition solution layers link below the command name
       to view the solution(s) that installed a definition of the command.




     2. The Solution Layers pane will display the layering of each ribbon component
       definition a particular solution has installed. The layer at the top of the list is the
       current definition that is used by the application, the other layers are inactive and
       aren't used by the application at the moment. If the top solution is uninstalled or an
       updated version is installed that removes the definition, then the next layer will
       become the current active definition used by the application. When an unmanaged
       Active solution layer is present, it will always be the definition the application uses. If
       there's no Active solution listed, then the solution listed at the top of the list will be
       the definition used by the application. Any custom-managed solutions that aren't
       published by Microsoft will also take precedence over Microsoft published solution
       layers.

       The Entity context indicates the object the ribbon customization is on, if "All Entities"
       is listed, then the layer is from the Application Ribbon client extensions and not
---

     entity specific, otherwise the logical name of the entity will be listed.

     When there are two or more layers, you can select two rows and select Compare to
     view a comparison of the definitions brought in by each solution.

     Selecting Back will return to the previous Command Checker window.

     The following image shows the solution layers for the command in our example, and
     indicates that there's a solution layer for the contact entity that it's an unmanaged
     customization as denoted by the solution titled Active. Your actual scenario may
     differ, you may not have an Active solution layer, you may have a managed solution
     and the name of that solution will be listed here.




   3. Now that we have reviewed the solution layers and identified the solution that
     installed the customization, we must fix the definition in the appropriate solution.

Select one of the following options that matches your particular scenario:
  The command is in the unmanaged Active solution

To delete a command in the Active unmanaged solution layer, we'll export an unmanaged
solution containing the entity or Application Ribbon and edit the <RibbonDiffXml> node in
the customizations.xml file, and then import a new version of this solution where this
command has been removed in order to delete the component. See Export, prepare to
edit, and import the ribbon.


The command is entity-specific

Based on our example scenario, we identified the entity is contact and the command that
needs to be deleted is Mscrm.NewRecordFromGrid and it's declared in the Active unmanaged
---

solution layer from a publisher named DefaultPublisherCITTest.

  1. Open Advanced Settings.

  2. Navigate to Settings > Solutions.

  3. Select New to create a new solution, set Publisher to the value shown in the
     Command Checker's solution layers listing for the command and the Active solution
     layer. (In our example, this is DefaultPublisherCITTest)

  4. Select Entities > Add Existing.

  5. Select the entity your command is defined on (In our example, this is contact) and
     select OK.

  6. Make sure you uncheck the Include entity metadata and Add all assets options
     before selecting Finish.

  7. Select Save.

  8. Select Export Solution and export the unmanaged solution.

  9. Extract the .zip file.

 10. Open the customizations.xml file.

 11. Locate the <Entity> node child of the entity node you wish to edit and locate its
     child <RibbonDiffXml> node.

 12. Locate the <CommandDefinition> node. (In our example, ID of the
     <CommandDefinition> node is Mscrm.NewRecordFromGrid , so we would locate the

     following node)
---

13. Edit the <RibbonDiffXml> node and remove the specific <CommandDefinition> node
   that has the ID of the command you wish to delete. Make sure you don't
   unintentionally delete other <CommandDefinition> nodes that may be present. (Based
   on our example, we would delete the <CommandDefinition> node in which ID is
    Mscrm.NewRecordFromGrid .)




14. Save the customizations.xml file.

15. Add the modified customizations.xml file back to the solution .zip file.

16. Import the solution file.
---

 17. Select Publish All Customizations.


The command is in the Application Ribbon (applies to "All entities")

If the command isn't entity-specific, rather it's applicable to "All Entities" declared in the
Application Ribbon, then the steps will be slightly different as follows:

   1. Open Advanced Settings.
   2. Navigate to Settings > Solutions.
   3. Select New to create a new solution, set Publisher to the value shown in the
     Command Checker's solution layers listing for the command and the Active solution
     layer.
   4. Select Client Extensions > Add Existing > Application Ribbons.
   5. Select Save.
   6. Select Export Solution and export the unmanaged solution.
   7. Extract the .zip file.
   8. Open the customizations.xml file.
   9. Locate the root <RibbonDiffXml> node.
 10. Locate the <CommandDefinition> node.
 11. Edit the <RibbonDiffXml> node and remove the <CommandDefinition> node that has
     the ID of the command you wish to delete. Make sure you don't unintentionally
     delete other <CommandDefinitions> nodes that may be present.
 12. Save the customizations.xml file.
 13. Add the modified customizations.xml file back to the compressed solution .zip file.
 14. Import the solution file.
 15. Select Publish All Customizations.
  The command is from a custom-managed solution that my company authored

To delete a command that was installed by a custom-managed solution that you created,
follow these steps:

   1. In your separate development organization that has the unmanaged source version
     of your custom solution, complete the steps listed above for the The command is in
     the unmanaged Active solution option.
   2. Increment the Version of your custom solution.
   3. Export solution as managed.
   4. In your separate affected organization, import this new version of your custom-
     managed solution.

  The command is from a custom-managed solution that my company did not author
(from third-party/ISV)
---

To delete a command that was installed by a custom-managed solution that was created
by a third-party/ISV, you'll need to contact the author of the solution and request a new
version of the solution that has removed the specific command definition and then install
this new solution into your affected organization.
---

A button on the command bar is visible
when it should be hidden
Article • 09/25/2023


Applies to: Power Apps
Original KB number: 4552163



Determine why a button is visible
A button will be made visible if all the enable rules and display rules on the command
associated with the button evaluate to true. If this is unexpected, it's possible that the
command definition has been overridden and is missing enable rules or display rules, or
the rule definitions themselves are overridden and causing the button to be visible when
you expect it to be hidden.


  ７ Note

  Some buttons are not customizable. For more information, see Non-customizable
  buttons in ribbon.



  ２ Warning

  Do not remove the Mscrm.HideOnModern display rule from a command to force a
  button to appear in the Unified Interface. Commands that have the
   Mscrm.HideOnModern display rule are intended for the legacy Web Client interface

  and are not supported in the Unified Interface, and may not work correctly.


   1. Enable Command checker and select the command button to inspect.

   2. The following example shows two Appointment buttons on the activities grid
      page, and one is expected to be hidden.
---

3. Select the Command Properties tab to display the details of the command for this
  button. This will display the actions, enable rules, and display rules, along with the
  result (True, False, Skipped) of each rule evaluation. Review the enable rules and
  display rules, if you expect a particular rule should be evaluating to false, then it's
  possible the rule is incorrectly customized or the necessary circumstances to return
  a false result aren't met. If so, skip to step 9, otherwise it's possible then that the
  command is missing a rule or rules and we'll view the command solution layers for
  further analysis.




4. Select the View command definition solution layers link below the command
  name to view the solution(s) that installed a definition of the command.
---

5. The Solution Layers pane will display the layering of each ribbon component
  definition a particular solution has installed. The layer at the top of the list is the
  current definition that is used by the application, the other layers are inactive and
  aren't used by the application at the moment. If the top solution is uninstalled or
  an updated version is installed that removes the definition, then the next layer will
  become the current active definition used by the application. When an unmanaged
  Active solution layer is present, it will always be the definition the application uses.
  If there's no Active solution listed, then the solution listed at the top of the list will
  be the definition used by the application. Any custom-managed solutions that
  aren't published by Microsoft will also take precedence over Microsoft published
  solution layers.

  The Entity context indicates the object the ribbon customization is on, if "All
  Entities" is listed, then the layer is from the Application Ribbon client extensions
  and not entity specific, otherwise the logical name of the entity will be listed.

  When there are two or more layers, you can select two rows and select Compare
  to view a comparison of the definitions brought in by each solution.

  Selecting Back will return to the previous Command Checker window.

  If there's only one solution layer, skip to step 9, otherwise, select the top two
  solution layers (If you have a layer in the Active solution, but it isn't listed at the
  top, select the Active solution layer and then the top row) and select Compare.
---

6. The comparison of the current active definition and the previous inactive definition
  will be displayed showing the differences, if any. The following example shows the
  unmanaged Active definition to have been customized with the removal of a
  display rule Mscrm.HideOnModern that is included in the inactive
  msdynce_ActivitiesPatch Microsoft published solution layer.




7. The approach needed to fix a button's visibility will depend on the various
  customizations in your specific scenario. If you determined that a rule is incorrectly
  evaluating to false, and if the rule definition is incorrectly defined, then you should
  modify the rule definition and make changes that would permit the rule to
  evaluate to false under the proper circumstances. If the rule definition is correct,
---

     then it's possible that the requirements that would make the rule return false aren't
     met, such as a field value or security privilege isn't correctly assigned. Depending
     on your rule definition, the requirements can vary greatly, refer to Define ribbon
     enable rules, and Define ribbon display rules. Considering our example, the
     command was customized with the removal of a Mscrm.HideOnModern display rule.
     This display rule is intended to hide this particular button from being displayed in
     Unified Interface applications and only be visible in the legacy Web Client interface.
     We could modify the custom version of the command and add the missing the
      Mscrm.HideOnModern display rule to the command definition. Since this is a custom

     override of a Microsoft published definition and there are no other intentional
     modifications, it's recommended that this custom version of the command be
     deleted to restore the default functionality.



Repair Options
Select a repair option from one of the tabs below. The first tab is selected by default.


 Delete the command




  How to delete a command
  If there's another solution layer that contains a working definition of this command,
  then you can delete this definition to restore the next inactive working definition.

  If this is the only layer and you no longer need the command, then you can remove
  it from your solution if no other button is referencing the command.

  Select one of the following options that matches your particular scenario:
    The command is in the unmanaged Active solution

  To delete a command in the Active unmanaged solution layer, we'll export an
  unmanaged solution containing the entity or Application Ribbon and edit the
  <RibbonDiffXml> node in the customizations.xml file, and then import a new version

  of this solution where this command has been removed in order to delete the
  component. See Export, prepare to edit, and import the ribbon.


  The command is entity-specific

  Based on our example scenario, we identified the entity is activitypointer and the
  command that needs to be deleted is Mscrm.CreateAppointment and it's declared in
---

the Active unmanaged solution layer from a publisher named
DefaultPublisherCITTest.

  1. Open Advanced Settings.

  2. Navigate to Settings -> Solutions.

  3. Select New to create a new solution, set Publisher to the value shown in the
     Command Checker's solution layers listing for the command and the Active
     solution layer. (In our example, this is DefaultPublisherCITTest).

  4. Select Entities > Add Existing.

  5. Select the entity your command is defined on (In our example, this is
     activitypointer) and select OK.

  6. Make sure you uncheck the Include entity metadata and uncheck Add all
     assets options before selecting Finish.

  7. Select Save.

  8. Select Export Solution and export the unmanaged solution.

  9. Extract the .zip file.

 10. Open the customizations.xml file.

 11. Locate the <Entity> node child of the entity node you wish to edit and locate
     its child <RibbonDiffXml> node.

 12. Locate the <CommandDefinition> node (In our example, ID of the
     <CommandDefinition> node is Mscrm.CreateAppointment , so we would locate

     the following node).
---

 13. Edit the <RibbonDiffXml> node and remove the specific <CommandDefinition>
    node that has the ID of the command you wish to delete. Make sure you don't
    unintentionally delete other <CommandDefinition> nodes that may be present.
    (Based on our example, we would delete the <CommandDefinition> node in
    which ID is Mscrm.CreateAppointment .)




 14. Save the customizations.xml file.

 15. Add the modified customizations.xml file back to the solution .zip file.

 16. Import the solution file.

 17. Select Publish All Customizations.


The command is in the Application Ribbon (applies to "All
entities")
---

If the command isn't entity-specific, rather it's applicable to "All Entities" declared in
the Application Ribbon, then the steps will be slightly different as follows:

   1. Open Advanced Settings.
   2. Navigate to Settings > Solutions
   3. Select New to create a new solution, set Publisher to the value shown in the
     Command Checker's solution layers listing for the command and the Active
     solution layer.
   4. Select Client Extensions > Add Existing > Application Ribbons.
   5. Select Save.
   6. Select Export Solution and export the unmanaged solution.
   7. Extract the .zip file.
   8. Open the customizations.xml file.
   9. Locate the root <RibbonDiffXml> node.
 10. Locate the <CommandDefinition> .
 11. Edit the <RibbonDiffXml> node and remove the <CommandDefinition> node
     that has the ID of the command you wish to delete. Make sure you don't
     unintentionally delete other <CommandDefinition> nodes that may be present.
 12. Save the customizations.xml file.
 13. Add the modified customizations.xml file back to the compressed solution .zip
     file.
 14. Import the solution file.
 15. Select Publish All Customizations.
  The command is from a custom-managed solution that my company authored

To delete a command that was installed by a custom-managed solution that you
created, follow these steps:

   1. In your separate development organization that has the unmanaged source
     version of your custom solution, complete the steps listed above for the The
     command is in the unmanaged Active solution option.
   2. Increment the Version of your custom solution.
   3. Export solution as managed.
   4. In your separate affected organization, import this new version of your
     custom-managed solution.

  The command is from a custom-managed solution that my company did not
author (from third-party/ISV)

To delete a command that was installed by a custom-managed solution that was
created by a third-party/ISV, you'll need to contact the author of the solution and
---

  request a new version of the solution that has removed the specific command
  definition and then install this new solution into your affected organization.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

A button on the command bar isn't
working correctly in Power Apps
Article • 09/25/2023


Applies to: Power Apps
Original KB number: 4552163



Determine why a button isn't working correctly
Several factors can cause a button action to fail. These include invalid ribbon
customizations in which the button's associated command definition is incorrectly
declared.


  ２ Warning

  Do not remove the Mscrm.HideOnModern display rule from a command to force a
  button to appear in the Unified Interface. Commands that have the
   Mscrm.HideOnModern display rule are intended for the legacy Web Client interface

  and are not supported in the Unified Interface. Therefore, they might not work
  correctly.


If a command isn't correctly declared, selecting a button might either do nothing or
display an error message.

Select one of the following options that best matches your situation to help us provide
the best resolution. The first tab is selected by default.


 Button does nothing when selected




  Fix a button that does nothing when selected
  When a button is selected and nothing occurs, this is typically caused by an
  incorrect configuration of the command that's associated with the button.

  The following are typical command configuration mistakes that are made when
  declaring the JavaScriptFunction value for the action. These mistakes can cause a
  button to malfunction and seem as though it does nothing when selected.
---

     Invalid FunctionName: The name of the JavaScript function doesn't match a
     valid function name in the JavaScript web resource that's assigned to the
     Library property.
     Invalid Library: This path isn't referring to a valid JavaScript web resource or
     isn't prefixed with $webresource: .
     Missing parameters: The JavaScript function is expecting specific parameters,
     and the command definition doesn't declare them.
     Incorrect parameter type or order: The parameters are declared by using an
     incorrect type or are in a different order than the one in which they're listed in
     the JavaScript function declaration.

Refer to Define ribbon actions for more configuration help.

If these configurations are correct, a JavaScript code error might be the cause. If the
custom JavaScript function is coded incorrectly and doesn't invoke the expected
behavior, the button won't work as expected. If you find one of the listed
configuration mistakes, fix the command definition to resolve the issue. Otherwise,
you might have to debug and fix the JavaScript function code to make the button
work correctly.

Identify what the button command is and which solution installed the bad
definition.

   1. Enable Command checker and select the command button to inspect.

   2. Select the Command Properties tab to display the details of the command for
     this button.




   3. The Command properties tab displays the actions and the corresponding
      JavaScriptFunction configuration. Select the View command definition

     solution layers link below the command name to view the solutions that
     installed a definition of the command.
---

4. The Solution Layers pane displays the layering of each ribbon component
  definition a particular solution has installed. The layer at the top of the list is
  the current definition that's used by the application. The other layers are
  inactive and aren't used by the application at the moment. If the top solution
  is uninstalled or an updated version is installed that removes the definition,
  then the next layer will become the current active definition that's used by the
  application. If an unmanaged Active solution layer is present, it will always be
  the definition that the application uses. If there's no Active solution listed, then
  the solution listed at the top of the list will be the definition that's used by the
  application. Any custom-managed solutions that aren't published by Microsoft
  will also take precedence over Microsoft-published solution layers.

  The Entity context indicates the object that the ribbon customization is on. If
  "All Entities" is listed, then the layer is from the Application Ribbon client
  extensions and not entity specific. Otherwise, the logical name of the entity
  will be listed.

  When there are two or more layers, you can select two rows and select
  Compare to view a comparison of the definitions that are provided by each
  solution.

  Selecting Back returns you to the previous Command Checker window.

  If there's only one solution layer, go to step 8. Otherwise, select the top two
  solution layers. (If you have a layer in the Active solution, but it's not listed at
  the top, select the Active solution layer, and then the top row.) Then, select
  Compare.
---

   5. The comparison of the current active definition and the previous inactive
     definition are displayed and will show the differences, if any. The following
     example shows that the unmanaged Active definition was customized by
     specifying the FunctionName value incorrectly, as compared to the other
     inactive definition in the Microsoft-published System solution layer. The
     FunctionName value is expected to be
     XrmCore.Commands.Delete.deletePrimaryRecord , but the custom definition has

     declared FunctionName="deletePrimaryRecord" . In this case, nothing will occur
     when the button is selected because the function can't be found.




                                                                                  


   6. The approach that's required to fix the action functionality of a button will
     depend on the various customizations in your specific scenario. Considering
     the example, the command was customized by specifying an incorrect
     FunctionName value. You could modify the custom version of the command,

     and fix the FunctionName value. Because this is a custom override of a
     Microsoft-published definition, and there are no other intentional
     modifications, we recommend that you delete this custom version of the
     command to restore the default functionality.

Select one of the following repair options.
---

Option 1: Delete the command that has the incorrect
JavaScriptFunction declaration
  The command is in the unmanaged Active solution.

To delete a command in the Active unmanaged solution layer, you'll export an
unmanaged solution containing the entity or Application Ribbon and edit the
<RibbonDiffXml> node in the customizations.xml file, and then import a new version

of this solution where this command has been removed in order to delete the
component. See Export, prepare to edit, and import the ribbon.


The command is entity-specific

Based on the example scenario, you determined that the entity is account, the
command that has to be deleted is Mscrm.DeletePrimaryRecord , and it's declared in
the Active unmanaged solution layer from a publisher that's named
DefaultPublisherCITTest.

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Select New to create a new solution, and set Publisher to the value that's
     shown in the Command Checker's solution layers listing for the command and
     the Active solution layer. (In the example, this is DefaultPublisherCITTest.)

   4. Select Entities > Add Existing.

   5. Select the entity that your command is defined on (in the example, this is
     "account"), and then select OK.

   6. Make sure that you clear the Include entity metadata and Add all assets
     options before you select Finish.

   7. Select Save.

   8. Select Export Solution, and export the unmanaged solution.

   9. Extract the .zip file.

 10. Open the customizations.xml file.

 11. Locate the <Entity> node child of the entity node that you want to edit, and
     locate its child <RibbonDiffXml> node.
---

12. Locate the <CommandDefinition> node. (In the example, the ID of the
    <CommandDefinition> node is Mscrm.DeletePrimaryRecord . Therefore, you

   would locate the following node.)




13. Edit the <RibbonDiffXml> node to remove the specific <CommandDefinition>
   node that has the ID of the command that you want to delete. Make sure that
   you don't unintentionally delete other <CommandDefinition> nodes that might
   be present. (Based on the example, you would delete the <CommandDefinition>
   node in which the ID is Mscrm.DeletePrimaryRecord .)




14. Save the customizations.xml file.

15. Restore the modified customizations.xml file to the solution .zip file.
---

 16. Import the solution file.

 17. Select Publish All Customizations.


The command is in the Application Ribbon (applies to "All
entities")

If the command isn't entity-specific but, instead, is applicable to "All Entities" that
are declared in the Application Ribbon, then the steps will be slightly different, as
follows:

   1. Open Advanced Settings.
   2. Navigate to Settings > Solutions.
   3. Select New to create a new solution, and set Publisher to the value that's
     shown in the Command Checker's solution layers listing for the command and
     the Active solution layer.
   4. Select Client Extensions > Add Existing > Application Ribbons.
   5. Select Save.
   6. Select Export Solution, and export the unmanaged solution.
   7. Extract the .zip file.
   8. Open the customizations.xml file.
   9. Locate the root <RibbonDiffXml> node.
 10. Locate the <CommandDefinition> node.
 11. Edit the <RibbonDiffXml> , and remove the <CommandDefinition> node that has
     the ID of the command that you want to delete. Make sure that you don't
     unintentionally delete other <CommandDefinition> nodes that might be
     present.
 12. Save the customizations.xml file.
 13. Restore the modified customizations.xml file to the compressed solution .zip
     file.
 14. Import the solution file.
 15. Select Publish All Customizations.
  The command is from a custom-managed solution that my company authored.

To delete a command that was installed by a custom-managed solution that you
created, follow these steps:

   1. In your separate development organization that has the unmanaged source
     version of your custom solution, complete the steps listed above for the The
     command is in the unmanaged Active solution option.
   2. Increment the Version of your custom solution.
   3. Export solution as managed.
---

   4. In your separate affected organization, import this new version of your
     custom-managed solution.
  The command is from a custom-managed solution that my company did not
author (from third-part or ISV).

To delete a command that was installed by a custom-managed solution that was
created by a third-party or ISV, you'll have to contact the author of the solution to
request a new version of the solution that has the specific command definition
removed, and then install this new solution in your affected organization.


Option 2: Fix the command JavaScriptFunction declaration
  The command is in the unmanaged Active solution.

To fix a command in the Active unmanaged solution layer, you'll export an
unmanaged solution that contains the entity or Application ribbon, edit the
<RibbonDiffXml> node in the customizations.xml file, and then import a new version

of this solution that contains the fixed command definition. See Export, prepare to
edit, and import the ribbon.


  ２ Warning

  Do not remove Mscrm.HideOnModern display rule from a command to force a
  button to appear in the Unified Interface. Commands that have the
  Mscrm.HideOnModern display rule are intended for the legacy Web Client

  interface and are not supported in the Unified Interface, and might not work
  correctly.



The command is entity-specific

Based on the example scenario, you determined that the entity is account, the
command that has to be fixed is Mscrm.DeletePrimaryRecord , and it's declared in the
Active unmanaged solution layer from a publisher that's named
DefaultPublisherCITTest.

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Select New to create a new solution, and set Publisher to the value shown in
     the Command Checker's solution layers listing for the command and the
     Active solution layer. (In the example, this is DefaultPublisherCITTest.)
---

 4. Select Entities > Add Existing.

 5. Select the entity that your command is defined on (In the example, this is
   account), and then select OK.

 6. Make sure that you clear the Include entity metadata and Add all assets
   options before you select Finish.

 7. Select Save.

 8. Select Export Solution, and export the unmanaged solution.

 9. Extract the .zip file.

10. Open the customizations.xml file.

11. Locate the <Entity> node child of the entity node that you want to edit, and
   locate its child <RibbonDiffXml> node.

12. Locate the <CommandDefinition> node. (In the example, the ID of the
    <CommandDefinition> node is Mscrm.DeletePrimaryRecord . Therefore, you

   would locate the following node.)




13. Edit the <RibbonDiffXml> node, and make the necessary changes to the
    <CommandDefinition> node that will enable the command to function correctly

   under the correct circumstances to fix the command. For more information
   about how to declare commands, see Define ribbon commands, and Define
---

     ribbon actions. (Based on the example, you would modify the
      <CommandDefinition> node's JavaScriptFunction by setting the FunctionName

     value to XrmCore.Commands.Delete.deletePrimaryRecord .)




 14. Restore the modified customizations.xml file to the solution .zip file.

 15. Import the solution file.

 16. Select Publish All Customizations.


The command is in the Application Ribbon (applies to "All
entities")

If the command isn't entity-specific but, instead, is applicable to "All Entities" that
are declared in the Application Ribbon, then the steps will be slightly different, as
follows:

   1. Open Advanced Settings.
   2. Navigate to Settings > Solutions.
   3. Select New to create a new solution, and set Publisher to the value that's
     shown in the Command Checker's solution layers listing for the command and
     the Active solution layer.
   4. Select Client Extensions > Add Existing > Application Ribbons.
   5. Select Save.
   6. Select Export Solution and export the unmanaged solution.
   7. Extract the .zip file.
   8. Open the customizations.xml file.
   9. Locate the root <RibbonDiffXml> node.
---

 10. Locate the <CommandDefinition> .
 11. Edit the <RibbonDiffXml> node to make the necessary changes to the
     <CommandDefinition> node that will enable the command to function correctly

     under the correct circumstances to fix the command. For more information
     about how to declare commands, see Define ribbon commands, and Define
     ribbon actions.
 12. Save the customizations.xml file.
 13. Restore the modified customizations.xml file to the compressed solution .zip
     file.
 14. Import the solution file.
 15. Select Publish All Customizations.
  The command is from a custom-managed solution that I authored.

To fix a command that was installed by a custom-managed solution that you
created, follow these steps:

   1. In your separate development organization that has the unmanaged source
     version of your custom solution, complete the steps listed above for the The
     command is in the unmanaged Active solution option.
   2. Increment the Version of your custom solution.
   3. Export solution as managed.
   4. In your separate affected organization, import this new version of your
     custom-managed solution.

  The command is from a custom-managed solution that I did not author or that
my organization does not own (from a third-party/ISV).

To fix a command that was installed by a custom-managed solution that was
created by a third-party or ISV, you'll have to contact the author of the solution to
request a new version of the solution that contains the fixed command definition,
and install this new solution in your affected organization.


I receive script error message: "Invalid JavaScript
Action Library"](#tab/error)

Fix a button that displays an error when selected
If a ribbon command bar button is selected and an error occurs, the error is
typically caused by incorrect ribbon command customizations.


Fix Script Error "Invalid JavaScript Action Library"
---

You might receive a script error message that resembles the following:

  Invalid JavaScript Action Library: [script name] is not a web resource and is not
  supported.




This is caused by an invalid ribbon command customization that has declared an
incorrect Library on the command's JavaScriptFunction .

   1. Enable Command checker and select the command button to inspect.

   2. The following example shows the New button on the account entity's form
     page is visible and is represented by an item labeled New.




   3. Select the Command Properties tab to display the details of the command for
     this button. This will display the Actions and JavaScriptFunction declaration,
     and any enable or display the rules together with the result (True, False,
     Skipped) of each rule evaluation.

     Expand JavaScriptFunction, by selecting the "chevron"       icon to view the
     details of the function declaration. The Library property must be a JavaScript
---

  web resource and be prefixed with $webresource: . The following example
  shows that the Library property is _/_static/common/scripts/RibbonActions.js.
  This isn't a path to a valid JavaScript web resource. You should next review the
  solution layers of the command to try to identify the correct value to fix the
  issue.




4. Select the View command definition solution layers link below the command
  name to view the solutions that installed a definition of the command.




5. The Solution Layers pane will display the layering of each ribbon component
  definition a particular solution has installed. The layer at the top of the list is
  the current definition that's used by the application, the other layers are
  inactive and aren't used by the application at the moment. If the top solution
  is uninstalled or an updated version is installed that removes the definition,
  then the next layer will become the current active definition used by the
  application. When an unmanaged Active solution layer is present, it will always
  be the definition the application uses. If there's no Active solution listed, then
  the solution listed at the top of the list will be the definition used by the
---

  application. Any custom-managed solutions that aren't published by Microsoft
  will also take precedence over Microsoft-published solution layers.

  The Entity context indicates the object the ribbon customization is on, if "All
  Entities" is listed, then the layer is from the Application Ribbon client
  extensions and not entity specific, otherwise the logical name of the entity will
  be listed.

  When there are two or more layers, you can select two rows and select
  Compare to view a comparison of the definitions brought in by each solution.

  Selecting Back will return to the previous Command Checker window.

  The following image shows the solution layers for the command in the
  example, and indicates that there's two solution layers, and one is an
  unmanaged customization as denoted by the solution titled Active and the
  other is from the System solution published by Microsoft. Your actual scenario
  might differ, you might not have an Active solution layer, you might have a
  managed solution and the name of that solution will be listed here.

  Select the top two rows and select Compare to view a comparison of the
  definitions brought in by each solution. If you only have one solution layer,
  then you'll skip this step.




6. The comparison between command definitions will show any differences that
  might exist between the two layers. The following example clearly shows that
  the Library value is different. The unmanaged entry from the Active solution is
  set to an incorrect path _/_static/common/scripts/RibbonActions.js (your
  specific path might be slightly different), and the default definition from
  Microsoft has set the library to $webresoure:Main_system_library.js . This is a
  supported path for this particular command (this value might be different,
---

     depending on your particular command). The only supported path is one that
     begins with $webresource: and ends with the name of a valid JavaScript web
     resource.




   7. Now that you have reviewed the solution layers and determined the solution
     that installed the customization, you must fix the definition in the appropriate
     solution.

Select one of the following options that matches your particular scenario:
  The command is in the unmanaged Active solution.

The approach to fix the command will vary depending on whether your definition is
the only one, or if there are other inactive definitions, and whether the changes
were intentional.

Select the option that reflects your scenario:

        The command does not have any intentional modifications, and I want to
     remove this custom layer.

     To delete a command in the Active unmanaged solution layer, you'll export an
     unmanaged solution that contains the entity or Application Ribbon, edit the
      <RibbonDiffXml> node in the customizations.xml file, and then import a new

     version of this solution where this command has been removed in order to
     delete the component. See Export, prepare to edit, and import the ribbon.

     The command is entity-specific
---

Based on the example scenario, you determined that the entity is account, the
command that has to be deleted is Mscrm.NewRecordFromForm , and it's declared
in the Active unmanaged solution layer from a publisher that's named
DefaultPublisherCITTest.

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Select New to create a new solution, and set Publisher to the value that's
     shown in the Command Checker's solution layers listing for the
     command and the Active solution layer. (In the example, this is
     DefaultPublisherCITTest.)

   4. Select Entities > Add Existing.

   5. Select the entity that your command is defined on. (In the example, this
     is account), and then select OK.

   6. Make sure that you clear the Include entity metadata and Add all assets
     options before you select Finish.

   7. Select Save.

   8. Select Export Solution, and export the unmanaged solution.

   9. Extract the .zip file.

 10. Open the customizations.xml file.

 11. Locate the <Entity> node child of the entity node that you want to edit,
     and locate its child <RibbonDiffXml> node.

 12. Locate the <CommandDefinition> node (In the example, ID of the
      <CommandDefinition> is Mscrm.NewRecordFromForm . Therefore, you would

     locate the following node.)
---

 13. Edit the <RibbonDiffXml> node to remove the specific
     <CommandDefinition> node. Make sure that you don't unintentionally

     delete other <CommandDefinition> nodes that might be present. (Based
     on the example, you would delete the <CommandDefinition> node in
     which the ID is Mscrm.NewRecordFromForm .)




 14. Save the customizations.xml file.

 15. Restore the modified customizations.xml file to the solution .zip file.

 16. Import the solution file.

 17. Select Publish All Customizations.

The command is in the Application Ribbon (applies to "All entities")
---

If the command isn't entity-specific but, instead, is applicable to "All Entities"
that are declared in the Application Ribbon, then the steps will be slightly
different, as follows:

   1. Open Advanced Settings.
   2. Navigate to Settings > Solutions.
   3. Select New to create a new solution, and set Publisher to the value that's
     shown in the Command Checker's solution layers listing for the
     command and the Active solution layer.
   4. Select Client Extensions > Add Existing > Application Ribbons.
   5. Select Save.
   6. Select Export Solution, and export the unmanaged solution.
   7. Extract the .zip file.
   8. Open the customizations.xml file.
   9. Locate the root <RibbonDiffXml> node.
  10. Locate the <CommandDefinition> node.
  11. Edit <RibbonDiffXml> to remove the <CommandDefinition> node that has
     the matching ID of the command that you want to delete. Make sure
     that you don't unintentionally delete other <CommandDefinition> nodes
     that might be present.
  12. Save the customizations.xml file.
  13. Restore the modified customizations.xml file to the compressed solution
     .zip file.
  14. Import the solution file.
  15. Select Publish All Customizations.
  The command has additional modifications that I want to retain, and I
want to fix this solution layer.

To fix a command in the Active unmanaged solution layer, you'll export an
unmanaged solution containing the entity or Application Ribbon and edit the
<RibbonDiffXml> node in the customizations.xml file, and then import a new

version of this solution containing the fixed command definition. See Export,
prepare to edit, and import the ribbon.


  ２ Warning

  Do not remove Mscrm.HideOnModern display rule from a command to
  force a button to appear in the Unified Interface. Commands that have
  the Mscrm.HideOnModern display rule are intended for the legacy Web
---

  Client interface and are not supported in the Unified Interface, and might
  not work correctly.


The command is entity-specific

Based on the example scenario, you determined that the entity is account, the
command that has to be fixed is Mscrm.NewRecordFromForm , and it's declared in
the Active unmanaged solution layer from a publisher that's named
DefaultPublisherCITTest.

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Select New to create a new solution, and set Publisher to the value
     shown in the Command Checker's solution layers listing for the
     command and the Active solution layer. (In the example, this is
     DefaultPublisherCITTest.)

   4. Select Entities > Add Existing.

   5. Select the entity that your command is defined on (In the example, this is
     account), and then select OK.

   6. Make sure that you clear the Include entity metadata and Add all assets
     options before you select Finish.

   7. Select Save.

   8. Select Export Solution, and export the unmanaged solution.

   9. Extract the .zip file.

 10. Open the customizations.xml file

 11. Locate the <Entity> node child of the entity node you want to edit, and
     locate its child <RibbonDiffXml> node.

 12. Locate the <CommandDefinition> node. (In the example, the ID of the
      <CommandDefinition> node is Mscrm.NewRecordFromForm . Therefore, you

     would locate the following node.)
---

13. Edit <RibbonDiffXml> to make the necessary changes to the
    <CommandDefinition> node that will enable the command to function

   correctly under the correct circumstances to fix the command. For more
   information about how to declare commands, see Define ribbon
   commands and Define ribbon actions. (Based on the example, you would
   modify the <CommandDefinition> node by setting
    Library="$webresoure:Main_system_library.js" , and then make sure that

   the FunctionName value matches. In the example, that would be
    FunctionName="XrmCore.Commands.Open.openNewRecord" .)




14. Save the customizations.xml file.

15. Restore the modified customizations.xml file to the solution .zip file.

16. Import the solution file.
---

       17. Select Publish All Customizations.

     The command is in the Application Ribbon (applies to "All entities")

     If the command isn't entity-specific, rather it's applicable to "All Entities"
     declared in the Application Ribbon, then the steps will be slightly different as
     follows:

        1. Open Advanced Settings.
        2. Navigate to Settings > Solutions.
        3. Select New to create a new solution, and set Publisher to the value that's
           shown in the Command Checker's solution layers listing for the
           command and the Active solution layer.
        4. Select Client Extensions > Add Existing > Application Ribbons.
        5. Select Save.
        6. Select Export Solution, and export the unmanaged solution.
        7. Extract the .zip file.
        8. Open the customizations.xml file.
        9. Locate the root <RibbonDiffXml> node.
       10. Locate the <CommandDefinition> node.
       11. Edit the <RibbonDiffXml> node to make the necessary changes to the
           <CommandDefinition> node that will enable the command to function

           correctly under the correct circumstances to fix the command. For more
           information about how to declare commands, see Define ribbon
           commands, and Define ribbon actions.
       12. Save the customizations.xml file.
       13. Restore the modified customizations.xml file to the compressed solution
           .zip file.
       14. Import the solution file.
       15. Select Publish All Customizations.
  The command is from a custom-managed solution that I authored.

To fix a command that was installed by a custom-managed solution that you
created, follow these steps:

   1. In your separate development organization that has the unmanaged source
     version of your custom solution, complete the steps listed above for the The
     command is in the unmanaged Active solution option.
   2. Increment the Version of your custom solution.
   3. Export solution as managed.
   4. In your separate affected organization, import this new version of your
     custom-managed solution.
---

     The command is from a custom-managed solution that I did not author or that
  my organization does not own (from a third-party or ISV).

  To fix a command that was installed by a custom-managed solution that was
  created by a third-party or ISV, you'll have to contact the author of the solution to
  request a new version of the solution that contains the fixed command definition,
  and then install this new solution in your affected organization.
     The command is in a Microsoft-published managed solution.

  To fix a command that was installed by a Microsoft-published managed solution,
  you might need to have a newer version of the solution be installed. This would
  typically be done during a release update. It's possible that you have identified a
  bug that still has to be fixed. Contact Customer Support for assistance.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

A button on the command bar has wrong
labels or translations
10/10/2025


This article resolves the wrong label or translation issue with a modern or classic command
button in Microsoft Power Apps.



Modern commands
You can customize labels and create translations for modern commands the same way as for
forms and tables. If a modern command shows incorrect text, its label might not have been
configured correctly.


Check if correct translations are present in the solution
Export translations for the solution that contains the modern command. Open the XML file and
verify that the label has the correct translations.

The following screenshot shows a translation file opened in Microsoft Excel. The last three rows
are for a modern command's description, tooltip, and label. The last two columns show the text
used for LCIDs 1033 and 2052, corresponding to English (United States) and Simplified Chinese
(China), respectively.




                                                                                               



Check solution layering
If the correct text is present in the translation file, there might be other solutions that override
it. View the solution layers for the label to check if there's text defined for the same label in a
higher solution.



Classic commands
You can customize labels and create translations for classic commands by adding them to the
<RibbonDiffXml> element of a customization.xml file and importing the XML file into a solution.
---

Check if correct translations are present
  1. Enable Command checker and select the command button to inspect.

  2. The right pane shows four kinds of text that can be customized for a command button.




                                                                                          


         Alt: The label used by screen readers.
         LabelText: The label displayed for the command button.
         ToolTipTitle: The tooltip heading of the command button.
         ToolTipDescription: The tooltip body text of the command button.

    For button label issues, the relevant property is LabelText.

  3. At the bottom of the text property, select View label solution layers. This option won't
    appear if the text hasn't been customized.
---

                                                                                         



    ７ Note

    Some label customizations for system commands don't use <RibbonDiffXml> and
    hence can't be inspected in Command checker.


4. Solutions that have customized the text are listed. In this example, only one solution has a
  customized LabelText.




                                                                                         
---

   5. Select the solution to see all the LocLabel translations it contains. Verify that the correct
     text is present.




                                                                                               



Check solution layering
If the correct LocLabel is present in a solution, there might be other solutions that override it.
View label solution layers and check if a higher solution has defined the same LocLabel.


Check if label IDs match exactly in the letter casing
Label IDs are case-sensitive when matching IDs in the ribbon XML to localized label values. The
button's LabelText should contain a valid LocLabel reference that exactly matches the casing of
the ID of a LocLabel record.


Regenerate command metadata
The Command checker might report the following error in the LocalizationErrors section:

  Missing object ID for translation lookup


Missing or incorrect metadata after a solution update can cause this error. To fix this issue,
regenerate the command metadata.



Reference
---

Command checker for model-driven app ribbons
---

Noncustomizable buttons in ribbon
09/11/2025


Applies to: Power Apps

The following buttons in the Unified Interface aren't implemented by ribbon customizations.
They're hardcoded by internal platform code and unfortunately aren't customizable. Therefore,
they aren't visible in the Ribbon Workbench     .

     Create view
     Help
     See all records
     Share
     Show as
     Show Chart
     Open Dashboards


  ７ Note

        The button with ID Mscrm.HomepageGrid.
        {!EntityLogicalName}.ChangeDataSetControlButton is a button intended only for Web

        client interface that's now deprecated and this is intentionally disabled in the Unified
        Interface. Any attempts to modify this button aren't supported.
        Microsoft doesn't provide help or support for community tools. To obtain support or
        help to use these programs, contact the program publisher.


Third-party information disclaimer

The third-party products that this article discusses are manufactured by companies that are
independent of Microsoft. Microsoft makes no warranty, implied or otherwise, about the
performance or reliability of these products.
---

Remove an active unmanaged layer of
the ribbon in Power Apps
Article • 02/09/2024


This article provides steps to remove the unmanaged layer of a ribbon component in
Microsoft Power Apps.



Use Command checker to remove an
unmanaged layer of a ribbon
Unmanaged customizations reside at the top layer of a component and subsequently
define the runtime behavior of the component. In most situations, you don't want
unmanaged customizations to determine the behavior of your components. To remove
the unmanaged layer of a ribbon component, follow these steps:

   1. Open the Command checker tool to delete unmanaged customizations for ribbon
      components.

      To enable Command checker, append the &ribbondebug=true parameter to the URL
      of your Dynamics 365 application. For example,
      https://yourorgname.crm.dynamics.com/main.aspx?appid=<ID>&ribbondebug=true .


   2. In the Command checker dialog, select a button and then select View button
      solution layers to find an unmanaged customization.

      For example, the New button shown in the following screenshot has an
      unmanaged customization.




                                                                                   
---

   3. Select the Remove active customization link next to the unmanaged layer.




                                                                                   


   4. Regenerate metadata once you delete the unmanaged layer.




                                                                                   



Remove an unmanaged layer of a ribbon
(manual procedure)
You can perform this manual procedure if the unmanaged ribbon customization you
want to remove isn't visible in the Command checker.

This process requires you to export an unmanaged solution containing the entity or
application ribbon, edit the <RibbonDiffXml> node in the customizations.xml file, and
then import a new version of this solution where this component was removed to delete
the component. For more information, see Export, prepare to edit, and import the
ribbon.



The ribbon component is entity-specific
Follow these steps if the component is declared for a specific entity:

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Open an existing solution or create a new solution.

     To create a new solution, follow these steps:
---

   a. Select New to create a new solution and set Publisher to your preferred
      publisher, or use your organization's default publisher if you're unsure.

   b. Select Entities > Add Existing.

   c. Select the entity your ribbon component is defined on and select OK.

   d. Make sure you clear the Include entity metadata and Add all Assets options
      before selecting Finish.

   e. Select Save.

4. Select Export Solution and export the unmanaged solution.

5. Extract the .zip file.

6. Open the customizations.xml file.

7. Locate the child node <Entity> of the entity node you want to edit, and then
  locate its child node <RibbonDiffXml> .

8. Locate the node to be deleted.

         To delete a command, you must locate the <CommandDefinition> node with
         the ID of the command you want to delete.
         To delete a HideCustomAction , you must locate the <HideCustomAction> node
         containing the ID of the item you want to remove.
         To delete an "Enable Rule" or "Display Rule," you must locate the
         <RuleDefinitions> node, and then locate the child node <EnableRule> or

         <DisplayRule> with the ID of the item you want to delete.

         To delete a button, you must locate the <CustomAction> node with the ID of
         the CustomAction you want to delete. Or, locate and delete the CustomAction
         node that contains the <button> , <splitbutton> , <flyoutanchor> , or <group>
         node with the ID of the control you want to delete.
         To delete a LocLabel , you must locate the <LocLabel> node with the ID of the
         LocLabel you want to delete.

         To delete all ribbon customizations for this entity, replace the
         <RibbonDiffXml> node with the default empty XML as shown in the Remove

         all unmanaged ribbon customizations section of this article.

9. Edit the <RibbonDiffXml> node and remove one or more appropriate nodes as
  described earlier. Make sure you don't unintentionally delete other nodes that
  might be present.
---

 10. Save the customizations.xml file.

 11. Add the modified customizations.xml file back to the solution .zip file.

 12. Import the solution file.

 13. Select Publish All Customizations.



The ribbon component is in the application
ribbon (applies to "All entities")
If the component isn't entity-specific but applies to "All Entities" declared in the
application ribbon, the steps are slightly different:

   1. Open Advanced Settings.

   2. Navigate to Settings > Solutions.

   3. Open an existing solution or create a new solution.

     To create a new solution, follow these steps:

      a. Select New to create a new solution and set Publisher to your preferred
         publisher, or use your organization's default publisher if you're unsure.

      b. Select Client Extensions > Add Existing > Application Ribbons.

      c. Select Save.

   4. Select Export Solution and export the unmanaged solution.

   5. Extract the .zip file.

   6. Open the customizations.xml file.

   7. Locate the root node <RibbonDiffXml> .

   8. Locate the node to be deleted.

            To delete a command, you must locate the <CommandDefinition> node with
            the ID of the command you want to delete.
            To delete a HideCustomAction , you must locate the <HideCustomAction> node
            containing the ID of the item you want to remove.
            To delete an "Enable Rule" or "Display Rule," you must locate the
            <RuleDefinitions> node, and then locate the child node <EnableRule> or
---

           <DisplayRule> with the ID of the item you want to delete.

          To delete a button, you must locate the <CustomAction> node with the ID of
          the CustomAction you want to delete. Or, locate and delete the CustomAction
          that contains the <button> , <splitbutton> , <flyoutanchor> , or <group> node
          with the ID of the control you want to delete.
          To delete a LocLabel , you must locate the <LocLabel> node with the ID of the
           LocLabel you want to delete.

          To delete all ribbon customizations for the application ribbon, replace the
           <RibbonDiffXml> node with the default empty XML as shown in the Remove

          all unmanaged ribbon customizations section of this article.

   9. Edit the <RibbonDiffXml> node and remove the appropriate node as described
     earlier. Make sure you don't unintentionally delete other nodes that might be
     present.

 10. Save the customizations.xml file.

 11. Add the modified customizations.xml file back to the compressed solution .zip file.

 12. Import the solution file.

 13. Select Publish All Customizations.



Remove all unmanaged ribbon customizations
To remove all unmanaged ribbon customizations for either a specific entity or
application ribbon, follow the preceding steps and replace the <RibbonDiffXml> node in
the solution's customizations.xml file with the following default empty XML declaration:

  XML


  <RibbonDiffXml>
     <CustomActions />
     <Templates>
        <RibbonTemplates Id="Mscrm.Templates"></RibbonTemplates>
     </Templates>
     <CommandDefinitions />
     <RuleDefinitions>
        <TabDisplayRules />
        <DisplayRules />
        <EnableRules />
     </RuleDefinitions>
     <LocLabels />
     </RibbonDiffXml>
---

Reference
Command checker




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

How to regenerate ribbon metadata
Article • 09/25/2023


Applies to: Power Apps

The following ribbon command bar issues are often caused by missing or incorrect
ribbon metadata:

      A button on the command bar is hidden when it should be visible.
      A button on the command bar is visible when it should be hidden.
      A button on the command bar is not working correctly.

An in-app tool, Command Checker, is available to help you regenerate all ribbon
metadata. Only system administrators, system customizers, and makers have the
permissions to regenerate metadata.



How to start the regeneration operation
You can use the Command Checker tool to start the regeneration of ribbon metadata.
To enable Command Checker, append the &ribbondebug=true parameter to your
Dynamics 365 application URL. For example:
https://yourorgname.crm.dynamics.com/main.aspx?appid=<ID>&ribbondebug=true .




                                                                                   


After Command Checker is enabled, a new special "Command Checker"          program
button is available within the application on each of the various command bars (global,
form, grid, and subgrid). (The button might be included on the More overflow flyout
menu). To open Command Checker, select the button on any command bar.




After the Command Checker dialog box opens, select the Regenerate ribbon metadata
button to start regenerating all the ribbon metadata.
---

On the confirmation prompt with instructions, select OK to start the regeneration.




How to check the operation status
After the ribbon metadata regeneration is triggered, a background operation begins.
You can check the status of the operation on the Solutions History page. (Open
Advanced Settings, and then navigate to Settings > Solutions > Solutions History.)




In Ribbon Metadata Generation Operations view, a RibbonMetadataGeneration
operation with the Started status is added, as follows.
---

                                                                                       



  ７ Note

  The operation will take several minutes to finish. After it finishes, the Status value
  will change to Completed, and the Result value will be set to Success or Failure, as
  appropriate.




                                                                                       


After the RibbonMetadataGeneration operation is completed successfully, clear your
browser cache, and then reopen your application to check for the issue again. If the
issue isn't resolved, you can follow the steps that are provided in ribbon troubleshoot
guidelines for additional mitigation information.



Reference
Command checker for model-driven app ribbons




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---

"Blocked a frame with origin" error
using Unified Interface apps
Article • 11/30/2022


Applies to: Power Apps



Symptoms
When you use Unified Interface apps in the Google Chrome browser or Google Android,
you receive the following error message:

  Blocked a frame with origin " https://<Site Name>.dynamics.com " from accessing a
  cross-origin frame.



Cause
It's a known issue that occurs in older versions of the Chrome browser and Chrome
WebView.



Workaround
To work around this issue, update the Chrome browser .


Get a Chrome update on the computer
Typically, updates are installed in the background when you close and reopen a web
browser. You can also manually check for an update for Chrome:

   1. On your computer, open Chrome.
   2. At the top right, select More.
   3. Select Help > About Google Chrome.
   4. To apply any available updates, select Relaunch.

The current version number is shown beneath the "Google Chrome" heading. Chrome
will check for updates when you're on this page.


Get a Chrome update in Android
---

Chrome should automatically update your Android-based device based on your Play
Store settings. You can check whether a newer version is available:

   1. On your Android phone or tablet, open the Play Store app.
   2. At the top right, tap the profile icon.
   3. Tap Manage apps & device.
   4. Under Updates available, locate Chrome.
   5. Next to Chrome, tap Update.

Third-party information disclaimer

The third-party products that this article discusses are manufactured by companies that
are independent of Microsoft. Microsoft makes no warranty, implied or otherwise, about
the performance or reliability of these products.




Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

Third-party cookies or pop-up blocker
errors when accessing Unified Interface
apps in a web browser
Article • 11/30/2022


Applies to: Power Apps



Symptoms
When you access Unified Interface apps in a web browser, you receive one of the
following error messages about cookies and pop-up blockers:

        Something has gone wrong. Check technical details for more details.
        Technical Details
        Session Id: <Session ID>
        Activity Id: <Activity ID>
        Timestamp: <Date Time> GMT-0700 (Pacific Daylight Time)
        {"errorInfo":{"code":"UserInterventionNeeded_CookiesBlocked",
        "localizedMessage":"Power Apps requires cookies to be enabled. Please enable
        them in your browser.","timestamp":<Time Stamp>,"description":"Power Apps
        requires cookies to be enabled. Please enable them in your browser."}} No
        stack available.


        A <Server Name> window was unable to open, and may have been blocked by
        a pop-up blocker. Please add this <Server Name> server to the list of sites
        your pop-up blocker allows to open new windows.



Cause
These issues occur because third-party cookies are blocked in the web browser.



Resolution
To check what browser you are using and the browser settings, go to
WhatIsMyBrowser        . Then, enable third-party cookies, and make sure that the related
sites are not blocked for cookies. For instructions for web browsers and iOS devices, see
troubleshooting startup issues for Power Apps.
---

Third-party information disclaimer

The third-party products that this article discusses are manufactured by companies that
are independent of Microsoft. Microsoft makes no warranty, implied or otherwise, about
the performance or reliability of these products.




Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---

No response from the back button in a
Unified Interface app
Article • 11/30/2022


Applies to: Power Apps



Symptoms
When you select the back button or the Save & Close button in a Unified Interface app,
there's no response. For example, when you select either button on an entity record
page, you expect to be returned to the previous page. However, you might have to
select the button several times until the program navigates to the desired page.




Cause
Browser history is shared by Unified Interface apps and iFrames of app forms. If you
create custom scripts in an iFrame that allow navigation or authentication redirection,
the iFrame adds extra history entries to the browser history. When you select the back
button or the Save & Close button on an entity record page, you're navigated to the
history entry that was added by the custom scripts from the iFrame instead of the entry
of the Unified Interface app. To navigate to the previous page, you have to select the
button several times to force the program to navigate through the history entries that
were added by the custom scripts from the iFrame.



Workaround
When you create custom scripts in iFrames, manage the Window.history        property to
remove any extra or unexpected history entries that are listed before the correct
backward navigation entry.
---

Feedback
Was this page helpful?     ﾂ Yes    ﾄ No


Provide product feedback      | Get help at Microsoft Q&A
---


## Troubleshooting Word templates

Troubleshooting Word templates
Article • 02/20/2025


This article helps you troubleshoot and resolve issues related to Word templates.



I'm unable to see an entity image in a Word
template for certain out-of-the-box and custom
entities

Reason
By default, only a few out-of-the-box entities—such as Account, Contact, Opportunity,
Order, Invoice, Product, Lead, Goal, and Territory—include an EntityImage value for the
Primary Image field, which you can use to upload the image to a Word template.
However, for other out-of-the-box (such as Quote, Business Unit, Appointment, and
Email) and custom entities, EntityImage isn't available.


Resolution
To show an image for entities that don't have an EntityImage by default, you create an
image field for the entity, upload the entity image to a record, and then add the entity
image to the Word template. In the following example, we add an EntityImage for a
Discuss contract renewal appointment.

To create an image field for the entity

   1. Go to Settings > Customizations > Customize the System.

   2. In the solution explorer, under Components, expand Entities, and then select the
      entity. In this example, we're selecting the Appointment entity.
---

3. In the Appointment entity, select Fields, and then select New.




4. In the new field form, enter Entity Image for the Display Name, enter EntityImage
  for the Name, and for Data Type, select Image.
---

  5. Save and close the form.

  6. Verify that the new field has been added by selecting the entity name. In this
     example, we've added Entity Image as a value for the Primary Image field for the
     Appointment entity.




  7. Publish the customizations.

To upload the entity image to the record
---

1. Open the entity record. In this example, we're opening a Discuss contract renewal
  appointment.




2. Select the image, and in the Choose Image dialog box, select Upload Image.




3. Select the image, and then select Change.
---

The image appears beside the entity.




To add the entity image to the Word template

  1. Download and open the word template.

     The downloaded template is saved in the following format:
     recordType organizationDateFormat time localDateFormat time.docx
     For example, the downloaded template name for the appointment is:
     Appointment 2020-7-15 15-39-27 17-7-2020 12-28-00 PM.docx.

  2. In the Developer tab, open XML Mapping Pane, right-click to select
     new_entityimage, and then select Insert Content Control > Picture.




     The entity image field with the image is added to the Word template.

  3. Save and upload the Word template to your Dynamics 365 Sales Hub app.
---

Now, when you download and open a document based on this template, it will contain
the image you added.


  ７ Note

  Similarly, if you add an image to an entity form, follow this process to upload the
  image to the Word template.




Some characters don't export correctly in
documents
Certain characters and sets of characters aren't supported in document export. When
these characters are in a document, the document exports successfully but the fields
and text that contains the characters between the unsupported character(s) are
removed. This behavior is by design to support compatibility across products between
Dynamics, Excel, Word, and Adobe PDF.

This table describes the characters not supported for document export.


                                                                               ﾉ   Expand table


 Character(s)     Description

 <                Less than symbol also used to indicate the start of an HTML element

 >                Greater than symbol also used to indicate the end of an HTML element

 &nbsp;           Non-breaking space HTML string


Here's an example of what happens when you export a document that contains
unsupported characters.

     1. There's this text in the Word document: Enter the user <account> number
     2. The document is exported from an app in Power Apps or a Dynamics 365 app.
     3. After the export: The <account> text in the example above is removed leaving the
       exported text as Enter the user number instead of Enter the user <account>
       number.


See also
Use Word templates to create standardized documents
---

Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Known issues with document

Known issues with document
management
Article • 02/20/2025


The customizations and configurations described here can cause issues with the
document management feature.



Components from an Iframe
Opening a component from an Iframe in an entity form from a Unified Interface app
won't succeed. For example, loading the Document Associated Grid for an entity form in
an Iframe loads the grid in the Iframe but users can't interact with the document records
from the grid.



Third-party solutions that modify Document
Management folders
Deploying third-party solutions that modify the folders used with the Document
Management feature can cause unexpected behavior. Examples include:

      Creation of entity record level SharePoint folders.
      Renaming of previously autocreated entity record level SharePoint folders.
      Moving previously autocreated entity record level SharePoint folders to another
      location.

If you experience unexpected behavior with the document management feature caused
by a third-party solution, contact the third-party solution vendor.



"File not found" error when adding a file from
a SharePoint site
If you receive a File not found error or encounter a problem while adding a file from a
SharePoint site or SharePoint subsite in customer engagement apps (Dynamics 365
Sales, Dynamics 365 Customer Service, Dynamics 365 Field Service, Dynamics 365
Marketing, and Dynamics 365 Project Service Automation), the likely cause is that you
have not created the document location records in the model-driven app to point to
these SharePoint document libraries and folders.
---

SharePoint document locations are records in model-driven apps, such as Dynamics 365
Sales and Customer Service, that point to a SharePoint document library or folder. To
use any SharePoint site or subsite in SharePoint integration, you must run the Document
Management Settings wizard once with the corresponding site URL, so that the
document libraries are created in the site.

To store documents for records, the document libraries or folders must be in place. If
model-driven apps are unable to create the document libraries and folders
automatically, you can manually create these in SharePoint. After you create the
document libraries and folders in SharePoint, you must create document location
records in model-driven apps to point to these SharePoint document libraries and
folders.

Learn more in Create or edit document location records.



"File not found" error when using multiple
SharePoint sites
If you receive a File not found error when using multiple SharePoint sites, the likely
cause is that there are no document libraries for a new SharePoint site. You must run the
Document Management Settings wizard for any newly added SharePoint sites.

The following steps describe the scenario that causes the error.

   1. Run the Document Management Settings wizard for the default SharePoint site.

   2. In the model-driven app in Dynamics 365, add a new SharePoint site (go to
     Advanced Settings > Document Management > SharePoint Sites > Add
     SharePoint Site). This creates a SharePoint site entry only in the application and
     doesn't create the document libraries in SharePoint that are required for document
     management.

   3. Open any entity where document management is enabled, and create the
     document location for the new site that you added in step 2 as the parent site.

   4. The "File Not Found" error is displayed. The cause of the error is that there are no
     document libraries for this new SharePoint site in SharePoint.

To mitigate this issue, run the Document Management Settings wizard for this newly
added site, as well.

Points to consider:
---

     Document management works only for entities that are selected while running the
     Document Management Settings wizard.

     The SharePoint site for which the Document Management Settings wizard is last
     run becomes the default site. You can reset the default site if required by running
     the Document Management Settings wizard again for that particular site.

For more information, see Create or edit document location records.



SharePoint enforces resource throttling with
5000 or more documents
A document library with 5000 or more documents might experience resource throttling.
Users may experience the following behavior with document management and
OneNote integration:

     A sort on columns other than the default sorted column, may return the error
     message "The throttling limit has been exceeded by this operation."
     Microsoft OneNote integration doesn't work when the document library has 5000
     or more documents.

If you have more than 5000 documents in your document library, you can view the
documents in the default grid view. For more information, see Manage large lists and
libraries in SharePoint   .



Relationship must be one-to-many (1:N)
between an entity and a SharePoint document
entity
Users can't see documents when many entities are pointing to a SharePoint document
location, a many-to-many relationship (N:N). The relationship must be one-to-many
(1:N) between any entity and a SharePoint document entity.

In Microsoft Dataverse, you can create an entity and enable the Document management
property for the entity. This allows for the entity to participate in integration with
SharePoint. Power Apps and Dataverse support only a one-to-many relationship (1:N)
between any entity and a SharePoint document-related entity. A many-to-one or a
many-to-many relationship between an entity and a SharePoint document entity results
in the app not listing the documents that exist in the SharePoint document library.
---

Document location for child entities
Documents of a child entity only appear in the parent documents folder when the
parent document location has been created. To create the location, navigate to the
Documents tab of the parent record. If no such location is created, child documents
don't appear in the parent entity folder. Once the location is created, child documents
begin to appear in the parent entity folder.



Document folder location for multiple lookups
If the entity selected for the Based on entity folder structure has two lookups,
documents can't be stored inside the entity folder, but can be stored in the root folder.
An example is when you have the Based on entity folder structure set to Account and
you have an entity with two lookup accounts like Work Order. The documents related to
Work Orders can't be stored inside any account document location, but can be stored in
the root folder.



Entering a date for OneNote documents
In order to add a date to a OneNote document, you can open the OneNote document
and double-click on the field under the title line. This allows you to enter the date field
and save the document.




SharePoint Document table doesn't display
inputs when you create a flow
When you create a Power Automate flow trigger on the Dataverse SharePoint
Documents table (named Documents in Power Automate), no data from the table is
passed to the flow editor. The flow inputs appear as an empty array.

This behavior occurs because the SharePoint Documents table is a virtual table and the
SharePoint and OneDrive document table data isn't stored in Dataverse. Below is an
example of a flow trigger using the SharePoint Documents table.
---

"Record is unavailable" message when you
attempt to open a file from the SharePoint
documents grid
This message might appear when a certain customization is made to the ribbon bar.
Ribbon customizations can be implemented by using a third-party tool called Ribbon
Workbench. When hiding a button on the ribbon bar, the Mscrm.OpenRecordItem
command might be hidden by using the tool, which can cause the error message.

To resolve the issue, follow these steps.

   1. Go to Power Apps     > Advanced settings > Settings > Customizations.

   2. Select the third-party tool Ribbon Workbench, then select the solution that
     contains the SharePoint document table.

   3. In the Entity dropdown list, select sharepointdocument.

   4. Under the Hide Actions dropdown list, right-click the
     Mscrm.OpenRecordItem.Hide action, and then select Un-Hide.
---

   5. Publish the solution.



Known issues

Document Associated Grid in child entity quick view form
The Document Associated Grid is designed to show documents related to the entity
context it's being rendered in. Embedding the Document Associated Grid in a related
(child) entity quick view form and configuring the grid to show documents from its
parent entity is unsupported.


SharePoint integration doesn't support the Dynamics 365
editable grid
SharePoint integration doesn't work with the Dynamics 365 editable grid, due to known
side effects that prevent SharePoint integration from working properly. Side effects
include: the document failing to load in the grid, an inability to create or upload
documents, and an inability to search in the grid.


Maximum number of rows not honored in the document
associated grid
Configuring the following in the DocumentGrid pane is ignored:
---

     Maximum number of rows: a value
     Use available space: unchecked

For Unified Interface and backward compatibility, the row limit in the document
associated grid is set to 5000 and Use available space is turned off. This behavior is a
known limitation.


Error message when opening a record: "The record
doesn't have a SharePoint location associated with it. Add
a SharePoint location."
This issue can occur when you're using the legacy list component for document
management. The list component isn't supported with the current versions of Power
Apps or Dynamics 365 apps.

In 2015, we announced the deprecation of the list component       .

If you're using the list component, you must move your document management to use
server-based authentication.

     For Power Apps and Dynamics 365 apps, see Switch from the list component or
     change the SharePoint deployment.
     For Dynamics 365 Customer Engagement (on-premises), see Switching from the
     list component or changing the deployment.


Error message "An error has occurred while loading
documents" when filtering by Name column
The error "An error has occurred while loading documents" is displayed. Reload the
document. If the problem persists, contact your Dynamics 365 administrator for help"
occurs when you filter by the Name column in the document associated grid.

This error occurs with the following filter by options in the document associated grid:

     Begins with
     Does not begin with
     Ends with
     Does not end with
---

This error occurs because these filter by options aren't currently supported with the
document associated grid.


Next and Previous page arrow buttons in the SharePoint
grid don't work
The Next and Previous page arrow buttons in the SharePoint grid don't work. This
behavior is a known issue.

Resolution: Users can select the Load More button at the bottom of the page or select
Open Location to go to the SharePoint site to access files.


OneDrive for Business configuration
OneDrive for Businees for new users can't be configured currently. This behavior is a
known issue and is planned to be fixed in a future release.


Removing support for Microsoft default service principal
In March 2025, support for connecting to the Dataverse virtual table sharepointdocument
using the Microsoft default service principal ends. This change is being made to improve
security. Switch to connect using a user account to prevent loss of access to the table.


Related content
Troubleshooting server-based authentication
Troubleshoot SharePoint integration
---

Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshooting server-based

Troubleshooting server-based
authentication
Article • 02/20/2025



Troubleshooting the Enable server-based
SharePoint Integration wizard
Review the error log for information about why the site doesn't validate. To do this, click
Error Log in the Enable Server-Based SharePoint Integration wizard after the validate
sites stage is completed.

The enable server-based SharePoint integration validation check can return one of the
following four types of failures.


Failed Connection
This failure indicates that the SharePoint server could not be accessed from where the
validation check was run. Verify that the SharePoint URL that you entered is correct and
that you can access the SharePoint site and site collection by using a web browser from
the computer where the Enable Server-Based SharePoint Integration wizard is running.
More information: Troubleshooting hybrid environments (SharePoint)


Failed Authentication
This failure can occur when one or more of the server-based authentication
configuration steps were not completed or did not complete successfully. More
information: Set up SharePoint integration

This failure can also occur if an incorrect URL is entered in the Enable Server-Based
SharePoint Integration wizard or if there is a problem with the digital certificate used for
server authentication. Similarly, this failure can occur as a result of a SharePoint site
rename when the URL is not updated in the corresponding SharePoint Site record. More
information: Users receive "You don't have permissions to view files in this location"
message


Failed authorization or 401 unauthorized error
---

This failure can occur when the claims-based authentication types do not match. For
example, in a hybrid deployment such as customer engagement apps to SharePoint on-
premises, when you use the default claims-based authentication mapping, the Microsoft
account email address used by the user must match the SharePoint user's Work email.
More information: Define custom claim mapping for SharePoint server-based
integration


SharePoint Version Not Supported
This failure indicates that the SharePoint edition, version, required service pack, or
required hotfix are missing.



Troubleshooting SharePoint
Issues that affect server-based authentication can also be recorded in SharePoint logs
and reports. For more information about how to view and troubleshoot SharePoint
monitoring, see the following topics. View reports and logs in SharePoint 2013 and
Configure diagnostic logging in SharePoint 2013



Known issues with server-based authentication
This section describes the known issues that may occur when you set up or use
customer engagement apps and SharePoint server-based authentication.


Failed authentication is returned when validating a
SharePoint site even though you have appropriate
permission
Applies to: customer engagement apps with SharePoint Online, customer engagement
apps with SharePoint on-premises.

This issue can occur when the claims-based authentication mapping that is used
provides a situation where the claims type values don't match between customer
engagement apps and SharePoint. For example, this issue can occur when the following
items are true:

     You use the default claims-based authentication mapping type, which for customer
     engagement apps to SharePoint Online server-based authentication uses the
     Microsoft account unique identifier.
---

     The identities used for Microsoft 365, Dynamics 365 administrator, or SharePoint
     Online administrator don't use the same Microsoft account, therefore the
     Microsoft account unique identifiers don't match.


"Private key not found" error message returned when you
run the CertificateReconfiguration.ps1 Windows
PowerShell script
This content also applies to the on-premises version.

This issue can occur when there are two self-signed certificates located in the local
certificate store that have the same subject name.

Notice that this issue should only occur when you use a self-signed certificate. Self-
signed certificates should not be used in production environments.

To resolve this issue, remove the certificates with the same subject name that you don't
need using the Certificate Manager MMC snap-in and note the following.


  ） Important

  It can take up to 24 hours before the SharePoint cache will begin using the new
  certificate. To use the certificate now, follow the steps here to replace the certificate
  information in customer engagement apps.

  To resolve this issue by following the steps in this article, the existing certificate
  cannot be expired.




Replace a certificate that has the same subject name

   1. Use an existing or create a new and self-signed certificate. The subject name must
     be unique to any certificate subject names that are registered in the local
     certificate store.

   2. Run the following PowerShell script against the existing certificate, or the
     certificate that you created in the previous step. This script will add a new
     certificate in customer engagement apps, which will then be replaced in a later
     step.

  PowerShell
---

      CertificateReconfiguration.ps1 -certificateFile <Private certificate file
   (.pfx)> -password <private-certificate-password> -updateCrm -certificateType
   AlternativeS2STokenIssuer -serviceAccount <serviceAccount> -storeFindType
   FindBySubjectDistinguishedName



   3. Remove the AlternativeS2STokenIssuer type certificate from the configuration
      database. To do this, run these PowerShell commands.

  PowerShell


     Add-PSSnapin Microsoft.Crm.PowerShell
     $Certificates = Get-CrmCertificate;
     $alternativecertificate = "";
     foreach($cert in $Certificates)
     {    if($cert.CertificateType -eq "AlternativeS2STokenIssuer") {
   $alternativecertificate = $cert;}   }

     Remove-CrmCertificate -Certificate $alternativecertificate




You receive "The remote server returned an error: (400)
Bad Request" and "Register-SPAppPrincipal: The
requested service,
<http://wgwitsp:32843/46fbdd1305a643379b47d761334f6134/
AppMng.svc> could not be activated" error messages

Applies to: SharePoint on-premises versions used with customer engagement apps.

The remote server returned an error: (400) Bad Request error message can occur after
the certificate installation, such as when you run the CertificateReconfiguration.Ps1
script.

The Register-SPAppPrincipal: The requested service,
<http://wgwitsp:32843/46fbdd1305a643379b47d761334f6134/AppMng.svc> could not be

activated error message can occur when you grant permission to access SharePoint by
running the Register-SPAppPrincipal command.

To resolve both of these errors after they occur, restart the web server where the web
application is installed. More information: Start or Stop the Web Server (IIS 8)


"Something went wrong while interaction with
SharePoint" error message received
---

Applies to: All versions when used with SharePoint Online

This error can be returned to the user who doesn't have site permissions or the user has
had permissions removed from the SharePoint site where document management is
enabled. Currently, this is a known issue with SharePoint Online where the error
message that is displayed to the user doesn't indicate that the user's permissions are
not sufficient to access the site.



How to display the Enable Server-Based
SharePoint Integration wizard
After server-based integration is enabled, the Enable Server-Based SharePoint
Integration wizard no longer appears in the Document Management area of Settings. To
display the Enable Server-Based SharePoint Integration wizard so that you can
reconfigure it, you must deactivate all SharePoint sites and disable OneDrive document
management.


Disable document management SharePoint sites and
OneDrive
   1. Sign into Power Apps, select Settings (gear) on the upper right, and then select
     Advanced settings.
   2. Go to Settings > Document Management > SharePoint Sites.
   3. In the view selector, select Active SharePoint Sites.
   4. Select all SharePoint sites in the list, on the command bar select Deactivate, and
     then select Deactivate at the message box prompt.




   5. Go to Settings > Document Management > Enable OneDrive for Business.
   6. Clear the Enable OneDrive for Business option, and then select OK.
---

After all SharePoint sites are deactivated and OneDrive integration is disabled, the
Enable Server-Based SharePoint Integration wizard will appear in the Document
Management area.


See also
Troubleshoot SharePoint Online integration
Permissions required for document management tasks




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshooting conditional access

Troubleshooting conditional access
authentication
Article • 02/20/2025


This article outlines how to address warning messages related to conditional access
authentication improvements for Manage your documents using SharePoint. These
warning messages will rollout soon notifying which users will be affected.

With security improvements in SharePoint integration authentication, you need to keep
SharePoint Online and Dataverse conditional access aligned to avoid issues. These
sections outline how to review and align conditional access.



Conditional access isn't enabled correctly
When the Document Associated grid shows a warning message "Conditional access isn't
enabled correctly", the error code at the end of the message guides addressing the
configuration.




SharePoint Document Grid warning AADSTS50076 or
AADSTS50079
When message shown is AADSTS50076 or AADSTS50079, an external security challenge
is required but not satisfied. A common cause is when multifactor authentication is
turned on for SharePoint, but not for Dataverse. Use these steps to ensure both are
aligned.

   1. Open the Microsoft Entra admin center to SharePoint Access Policy using Find
      SharePoint Online conditional access.
   2. Select Access controls > Grant to open the Grant dialog.
   3. Under Grant access, check if the Require multifactor authentication option, and
      optionally the Require authentication strength option, is selected.
   4. If either item is selected, then turn on the related Dataverse conditional access
      policy, if not already turned on, using Find Dataverse conditional access.
---

There are other situations which might cause this issue. If you checked and it's not
multifactor authentication-related, contact Microsoft support and open a ticket
requesting support.


SharePoint Document Grid warning AADSTS50158
When message shown is AADSTS50158, the error can be related to either multifactor
authentication or conditional access policy.

First, check if multifactor authentication is turned on in Dataverse following the steps in
AADSTS50076. Turn on Dataverse multifactor authentication if it's not already turned on.

If multifactor authentication is turned on in both Dataverse and SharePoint, then you
need to check SharePoint conditional access.

   1. When the device is managed, open Extra SharePoint Access Policy using Find
     SharePoint Online conditional access.
   2. Check if the device has any network conditions:
      a. Select the link under Network.
      b. Review network conditions selected under Include and Exclude.
   3. Check if the device is in locations conditions:
      a. Select the link under Conditions.
      b. Select the link under Locations.
      c. Review selected network or physical locations.


SharePoint Document Grid warning AADSTS53001
When message shown is AADSTS53001, the device isn't in a domain-joined status. Use
the following steps to resolve the issue.

   1. Log out or restart your device if you're already logged in.
   2. Sign in to your device using your work or school account.
   3. Connect to your organization's network through a virtual private network (VPN) or
     DirectAccess.
   4. Clear your browser's cache and restart the browser.
   5. Try to use the SharePoint integration feature again.


SharePoint Document Grid warning AADSTS53000
When message shown is AADSTS53000, a SharePoint conditional access policy is
preventing the device access to the resource. If blocked access is expected, inform the
user how to access within the conditional access policy. If blocked access isn't expected,
---

review the SharePoint conditional access within Microsoft Entra admin center
SharePoint Access Policy.

   1. Open the Microsoft Entra admin center to SharePoint Access Policy using Find
     SharePoint Online conditional access.
   2. Select Access controls > Grant to open the Grant dialog.
   3. Under Grant access, check if the Require device to be marked as compliant
     option or the Require Microsoft Entra hybrid joined device option is selected.


SharePoint Document Grid warning AADSTS530003
When message shown is AADSTS530003, the access is related to a device. First use
AADSTS53000 to check if the device is managed and then follow these steps.

   1. When the device is managed, open Extra SharePoint Access Policy using Find
     SharePoint Online conditional access.
   2. Check if the device is in the supported list:
      a. Select the link under Conditions.
      b. Select the link under Device platforms.
      c. Review platforms selected under Include and Exclude.
   3. Check if the device is in the supported list:
      a. Select the link under Conditions.
      b. Select the link under Client apps.
      c. Review the selected client apps and in particular the Browser client app.
   4. Check if the device is filtered:
   5. Select the link under Conditions.
   6. Select the link under Filter for devices.
   7. Review the filtered devices.


SharePoint Document Grid warning AADSTS500011
When message shown is AADSTS500011, the SharePoint on-premises integration isn't
configured correctly. The configuration steps in Configure server-based authentication
with SharePoint on-premises need to be reviewed carefully to maintain access.


  ７ Note

  First check configurations steps for SharePoint Server SPN in Microsoft Entra
  Domain Services steps 3, 4, and 5.
---

Authentication isn't enabled correctly
When the Document Associated grid shows a warning message "Authentication isn't
enabled correctly", contact support to confirm that authentication is turned on for the
environment.




Find conditional access setup

Find SharePoint Online conditional access
   1. Open Microsoft Entra     as a tenant admin.

   2. Select Applications > Enterprise Applications in the left menu.

   3. Clear the filter "Application type == Enterprise Applications".




   4. Search for Office 365 SharePoint Online and select the item in the list.




   5. Select Conditional Access to show the list of policy names.




   6. Select SharePoint Access Policy in the policy list.


Find Dataverse conditional access
   1. Open Microsoft Entra     as a tenant admin.

   2. Select Applications > Enterprise Applications in the left menu.

   3. Clear the filter "Application type == Enterprise Applications".
---

   4. Search for Dataverse and select it in the list.




   5. Select Conditional Access to show the list of policy names.




Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot SharePoint integration

Troubleshoot SharePoint integration
Article • 02/20/2025


This topic explains how to fix common issues that may occur with SharePoint document
management.



Missing Documents button - validate and fix
If Documents is missing from entities such as account, use the following to restore.




   1. Make sure you have the System Administrator security role or equivalent
      permissions. Check your security role: a. Follow the steps in View your user profile.
      b. Don't have the correct permissions? Contact your system administrator.

   2. Fix the missing Documents button. Follow these steps:
      a. Identity the entity for which the documents link should be visible (e.g. account,
            contact, opportunity...etc.).
      b. Go to Settings > Document Management Settings.
       c. Make sure the entity you wished to have documents link (selected in Step 1) are
            selected and a valid SharePoint URL is specified.
      d. Complete the wizard.
      e. Verify the Documents button appears.

For more information, see Enable SharePoint document management for specific
entities.



Malformed FetchXML or LayoutXML - validate
and fix
---

Malformed FetchXML or LayoutXML can cause any of the following issues:

     Documents associated grid is missing
     Unable to view folders
     Unable to view documents inside folders
     Document is not getting deleted
     Error Message – "Required parameter is null or undefined: url" while opening the
     documents tab
     Error Message – "System.NullReferenceException" while uploading a document
     Document being downloaded instead of opening in new tab

There can be many causes for FetchXML or LayoutXML to be malformed. The most
common cause is customizing the entity/grid view, adding/removing columns, and
other similar customizations.

If FetchXML or LayoutXML are malformed, use the following to restore.

   1. Make sure you have the System Administrator security role or equivalent
     permissions. Check your security role:
      a. Follow the steps in View your user profile.
     b. Don't have the correct permissions? Contact your system administrator.

   2. In the web app, go to Settings (      ) > Advanced Settings, go to Settings >
     Customizations > Solutions.

   3. Create a solution (named SharePointDocumentSolution). For more information, see
     Create a solution.

   4. Choose Entities > Add Existing > Entity > find and add SharePoint Document
     entity (select all fields, forms, views).

   5. Select Save and Close.

   6. Publish all customizations.

   7. Select the created (SharePointDocumentSolution) solution.

   8. Export the solution and choose the Package type as "Unmanaged".
     SharePointDocumentSolution.zip will be downloaded.

   9. Delete the solution that was created during step 3 from the organization.

 10. Extract the exported solution zip file (downloaded file from Step 8).

 11. In the solution contents folder, locate and then open Solution.xml.
---

12. Change the following value in Solution.xml, and then save it.
   From <Managed>0</Managed> to <Managed>1</Managed> .

13. In the solution contents folder, locate and open customization.xml.

14. Search the <SavedQuery> element where the savedqueryid attribute is equal to
   "0016f9f3-41cc-4276-9d11-04308d15858d".

15. If you can't find a saved query with the ID specified in the previous step, go to step
   19. However, if the <SavedQuery> element found in step 14 is similar to <SavedQuery
   unmodified="1"> , remove the unmodified="n" attribute.


16. Search layoutxml of Document associated grid (search for Document Associated).




17. Make the changes as indicated below for the layoutxml section:

      XML


      <layoutxml>
       <grid name="sharepointdocument" object="9507" jump="fullname"
      select="1" icon="0" preview="1">
        <row name="sharepointdocument" id="sharepointdocumentid">
              <cell name="fullname" width="300"
      imageproviderfunctionname="DocumentManagement.FileTypeIcon.loadSharePoi
      ntFileTypeIcon"
      imageproviderwebresource="$webresource:SharePoint_main_system_library.j
      s" />
              <cell name="modified" width="150" />
              <cell name="sharepointmodifiedby" width="150" />
              <cell name="locationname" width="150" />
              <cell name="relativelocation" width="200" />
              <cell name="servicetype" width="90" />
              <cell name="documentid" ishidden="1" />
              <cell name="title" ishidden="1" />
              <cell name="author" ishidden="1" />
              <cell name="sharepointcreatedon" ishidden="1" />
              <cell name="sharepointdocumentid" ishidden="1" />
              <cell name="filetype" ishidden="1" />
              <cell name="readurl" ishidden="1" />
              <cell name="editurl" ishidden="1" />
              <cell name="ischeckedout" ishidden="1" />
              <cell name="absoluteurl" ishidden="1" />
              <cell name="locationid" ishidden="1" />
              <cell name="iconclassname" ishidden="1" />
        </row>
---

       </grid>
      </layoutxml>




      ） Important

      All the attributes configured in the layout xml require their corresponding
      respective attributes to be present in the Fetch XML. The grid will return an
      error when this configuration is incorrect.


18. Make the changes as below for the FetchXml section:

      XML


      <fetch distinct="false" mapping="logical">
         <entity name="sharepointdocument">
           <attribute name="documentid" />
           <attribute name="fullname" />
           <attribute name="relativelocation" />
           <attribute name="sharepointcreatedon" />
           <attribute name="ischeckedout" />
           <attribute name="filetype" />
           <attribute name="modified" />
           <attribute name="sharepointmodifiedby" />
           <attribute name="servicetype" />
           <attribute name="absoluteurl" />
           <attribute name="title" />
           <attribute name="author" />
           <attribute name="sharepointdocumentid" />
           <attribute name="readurl" />
           <attribute name="editurl" />
           <attribute name="locationid" />
           <attribute name="iconclassname" />
           <attribute name="locationname" />
           <order attribute="relativelocation" descending="false" />
           <filter>
             <condition attribute="isrecursivefetch" operator="eq" value="0"
      />
           </filter>
         </entity>
      </fetch>



19. Similarly search the <SavedQuery> element where the savedqueryid attribute is
   equal to "a5b008ac-07d9-4554-8509-2c05767bff51".

20. If you can't find a saved query with the ID specified in the previous step, go to step
   24. However, if the <SavedQuery> element found in step 19 is similar to <SavedQuery
   unmodified="1"> , remove the unmodified="n" attribute.
---

21. Search layoutxml of All SharePoint Document (search for All SharePoint Document).




22. Make the changes as indicated below for the layoutxml section:

     XML


      <layoutxml>
        <grid name="sharepointdocument" jump="fullname" select="1" icon="0"
      preview="1">
          <row name="sharepointdocument" id="sharepointdocumentid">
            <cell name="fullname" width="300"
      imageproviderfunctionname="DocumentManagement.FileTypeIcon.loadSharePoi
      ntFileTypeIcon"
      imageproviderwebresource="$webresource:SharePoint_main_system_library.j
      s" />
            <cell name="relativelocation" width="200" />
            <cell name="modified" width="150" />
            <cell name="sharepointmodifiedby" width="150" />
            <cell name="sharepointcreatedon" width="300" />
            <cell name="documentid" ishidden="1" />
            <cell name="title" ishidden="1" />
            <cell name="readurl" ishidden="1" />
            <cell name="editurl" ishidden="1" />
            <cell name="author" ishidden="1" />
            <cell name="absoluteurl" ishidden="1" />
            <cell name="sharepointdocumentid" ishidden="1" />
            <cell name="filetype" ishidden="1" />
            <cell name="ischeckedout" ishidden="1" />
            <cell name="locationid" ishidden="1" />
            <cell name="iconclassname" ishidden="1" />
          </row>
        </grid>
      </layoutxml>



23. Make the changes as below for the FetchXml section:

     XML


      <fetch distinct="false" mapping="logical">
        <entity name="sharepointdocument">
          <attribute name="documentid" />
          <attribute name="fullname" />
          <attribute name="relativelocation" />
          <attribute name="sharepointcreatedon" />
          <attribute name="filetype" />
          <attribute name="absoluteurl" />
---

            <attribute name="modified" />
            <attribute name="sharepointmodifiedby" />
            <attribute name="title" />
            <attribute name="readurl" />
            <attribute name="editurl" />
            <attribute name="author" />
            <attribute name="sharepointdocumentid" />
            <attribute name="ischeckedout" />
            <attribute name="locationid" />
            <attribute name="iconclassname" />
            <filter>
              <condition attribute="isrecursivefetch" operator="eq" value="1"
      />
          </filter>
          <order attribute="relativelocation" descending="false" />
        </entity>
      </fetch>



24. Similarly search the <SavedQuery> element where the savedqueryid attribute is
   equal to "cb177797-b2ac-42a8-9773-5412321a965c".

25. If you can't find a saved query with the ID specified in the previous step, go to step
   29. However, if the <SavedQuery> element found in step 24 is similar to <SavedQuery
   unmodified="1"> , remove the unmodified="n" attribute.


26. Search layoutxml of OneNote SharePoint Document (search for OneNote
   SharePoint Document).




27. Make the changes as indicated below for the layoutxml section:

      XML


      <layoutxml>
        <grid name="sharepointdocument" jump="fullname" select="1" icon="0"
      preview="1">
          <row name="sharepointdocument" id="sharepointdocumentid">
            <cell name="fullname" width="300"
      imageproviderfunctionname="DocumentManagement.FileTypeIcon.loadSharePoi
      ntFileTypeIcon"
      imageproviderwebresource="$webresource:SharePoint_main_system_library.j
      s" />
            <cell name="relativelocation" width="200" />
            <cell name="modified" width="150" />
            <cell name="sharepointmodifiedby" width="150" />
            <cell name="sharepointcreatedon" width="300" />
---

            <cell name="title" ishidden="1" />
            <cell name="readurl" ishidden="1" />
            <cell name="editurl" ishidden="1" />
            <cell name="author" ishidden="1" />
            <cell name="absoluteurl" ishidden="1" />
            <cell name="filetype" ishidden="1" />
            <cell name="ischeckedout" ishidden="1" />
            <cell name="locationid" ishidden="1" />
            <cell name="iconclassname" ishidden="1" />
          </row>
        </grid>
      </layoutxml>



28. Make the changes as below for the FetchXml section:

      XML


      <fetch distinct="false" mapping="logical">
         <entity name="sharepointdocument">
           <attribute name="documentid" />
           <attribute name="fullname" />
           <attribute name="relativelocation" />
           <attribute name="sharepointcreatedon" />
           <attribute name="filetype" />
           <attribute name="modified" />
           <attribute name="sharepointmodifiedby" />
           <attribute name="title" />
           <attribute name="readurl" />
           <attribute name="editurl" />
           <attribute name="author" />
           <attribute name="absoluteurl" />
           <attribute name="ischeckedout" />
           <attribute name="locationid" />
           <attribute name="iconclassname" />
           <filter type="and">
             <condition attribute="documentlocationtype" operator="eq"
      value="1" />
             <condition attribute="isrecursivefetch" operator="eq" value="0"
      />
             <filter type="or">
               <condition attribute="filetype" operator="eq" value="one" />
               <condition attribute="filetype" operator="eq" value="onetoc2"
      />
             </filter>
           </filter>
           <order attribute="sharepointcreatedon" descending="true" />
         </entity>
      </fetch>



29. Save the file.

30. Zip the folder.
---

 31. Open a model-driven app in Dynamics 365.

 32. Navigate to Settings > Solutions

 33. Import the solution (zipped file in Step 8).

 34. Publish all customizations.

 35. Verify that any of the issues associated with the malformed FetchXML or
     LayoutXML are resolved. For example, verify that Document associated grid
     displays in all the required SharePoint documents.



Validate and fix SharePoint site URLs
In customer engagement apps (such as Dynamics 365 Sales and Customer Service),
SharePoint site and document location records contain links to site collections, site,
document libraries, and folders in SharePoint. These site and document location records
are associated with records so that the documents for records can be stored in
SharePoint.

When the links between customer engagement apps and SharePoint break, you must
validate and fix the links so that the records continue to point to the correct document
libraries and folders for managing the documents.

   1. Make sure you have the System Administrator security role or equivalent
     permissions in Microsoft Dynamics 365.

     Check your security role

           Follow the steps in View your user profile.

           Don’t have the correct permissions? Contact your system administrator.

   2. Find and fix the URLs. To do this, follow these steps.

      a. Go to Settings > Document Management.

     b. Click SharePoint Sites.

      c. Select the site URLs that you want to validate, and then click or tap Validate.

   3. Customer engagement apps validate all the selected site URLs and their immediate
     subordinate site and document library URLs. It then displays the results in
     Validating Sites.
---

   4. To fix a URL, open the site record, and enter the correct URL. More information:
     Create or edit site records.

   5. Click Save & Close.



Users receive "You don't have permissions to
view files in this location" message
This error message can occur when the SharePoint site that is configured with document
management has been renamed, but the SharePoint sites URL record has not been
updated to reflect the change.

   1. Go to Settings > Document Management > SharePoint Sites.

   2. Open the SharePoint Site record that has been renamed and enter the Absolute
     URL with new URL.




   3. Select Save & Close.


See also
Troubleshooting server-based authentication




Feedback
Was this page helpful?    Yes       No
---

Provide product feedback
---


## Troubleshooting document

Troubleshooting document
management issues
Article • 02/20/2025


This topic explains how to use information provided in error messages to fix issues with
the document management feature. Below is an index that will help you to reach the
right solution. The link in each cell navigates to the reason and mitigation steps for the
corresponding error message.



Error messages
The following are error messages that are possible with document management.


Error Message 1
Document library <entity name> has been renamed or deleted from SharePoint site
<SharePoint site> . Rerun the document management wizard and try again.



Error Message 2
Folder <folder name> has been renamed or deleted from SharePoint. It was expected
inside <folder path> path. Restore the folder on SharePoint and try again.



Index of errors
                                                                          ﾉ   Expand table


 Error                             Error Message 1                 Error Message 2

 Refresh the document grid for     Mitigation steps for missing    Mitigation steps for
 existing record                   document library                missing folder

 Load the document grid after      Mitigation steps for missing    Mitigation steps for
 creating new record               document library                missing folder

 Upload file                       Mitigation steps for missing    Mitigation steps for
                                   document library                missing folder

 Create new file/folder            Mitigation steps for missing    Mitigation steps for
                                   document library                missing folder
---

 Error                            Error Message 1                Error Message 2

 Add location                     Mitigation steps for missing   Mitigation steps for
                                  document library               missing folder

 Edit location                    Mitigation steps for missing   Mitigation steps for
                                  document library               missing folder




Reason and mitigation steps for missing
document library
Error message displayed for missing document library:

"Document library <entity name> has been renamed or deleted from SharePoint site
<SharePoint site> . Rerun the document management wizard and try again."


     Error message in Unified Interface:




     or




     Error message in the web client:
---

     or




     Log file:




Reason
This error typically occurs when the SharePoint document library was created for the
record. Because of some changes in SharePoint, the document library doesn't exist
anymore. This can happen because the document library was deleted or moved to a
different SharePoint site.


Mitigation steps for missing document library
   1. The error message shows the name of the document library that is missing. It also
     shows the path where the document library is expected on the SharePoint site.

   2. Select Settings -> Document Management Settings.

   3. Make sure the entity for the document library found from step 1 is selected and a
     valid SharePoint URL is specified.
---

   4. Complete the Document Management Settings wizard.

   5. The last step of wizard should have the status of document library as succeeded.




   6. Once complete, verify that document library is now present on the SharePoint site
     in the path shown in the error message.

   7. Launch the application and repeat the operation that produced the error.



Reason and mitigation steps for missing folder
Error message displayed for missing folder:

"Folder " <folder name> " has been renamed or deleted from SharePoint. It was expected
inside " <folder path> " path. Restore the folder on SharePoint and try again.

     Error message when the entity-based folder structure is not enabled.

     Folder path is ../<entity name>/<record name>

        Error message in Unified Interface:
---

  or




  Error message in the web client:




  or




  Log file:




Error message when the entity-based folder structure is enabled.
---

Folder path is ../<account or contact>/<account or contact name>/<entity
name>/<record name>


  Error message in Unified Interface:




  or




  Error message in the web client:




  or
---

        Log file:




Reason
This error typically occurs when the SharePoint folder was created for the record.
Because of a change in SharePoint, the folder doesn't exist anymore. This can happen
because the folder for this record was either renamed, deleted, or moved to different
location.


Mitigation steps for missing folder
   1. The error message shows the name of the folder which is missing. It also shows the
     path where the folder was expected on the SharePoint site. Navigate to this path in
     SharePoint.

   2. Create a new folder on SharePoint with the name the same as the folder name
     provided in error message.

   3. Once complete, verify that folder is now present on the SharePoint site in the path
     shown in the error message.

   4. Launch the application and repeat the operation that produced the error.


See also
Known issues with document management
---

Feedback
Was this page helpful?      Yes    No


Provide product feedback
---


## Troubleshoot offline sync errors in the

Troubleshoot offline sync errors in the
Power Apps mobile app
Article • 05/20/2024


Data sync can fail in offline-enabled mobile apps due to various errors. Depending on
the type of the app, the error message may vary.



Model-driven apps, including Field Service
If the offline sync status icon indicates a warning or error, you can tap on it to open the
Device Status page to see more details. On the Device Status page, you can see your
current device state and details of the last sync. If an error or warning occurs, you'll see a
message describing the issue.

For more information, see View offline sync status.



Canvas apps (preview)
In canvas apps, sync errors might occur when opening the app for the first time. A
dialog appears with an error message. For more information, see Work with canvas apps
offline (preview).



Offline sync errors
If you encounter an error while syncing offline data in the Power Apps mobile app, look
for the error message in the following table and contact your administrator or app
developer to perform the recommended action.

Make sure you have installed the latest version of the mobile app from the Google Play
Store, Apple App Store, or Microsoft Store.


                                                                                 ﾉ    Expand table


 Error message                                Recommended action

 Failed to download because we cannot         Verify that you have a strong internet connection
 connect to the server.                       and try again.

 It's taking a while to calculate data to     The sync for the table <tablename> times out.
 download (entity with timeout:               Consider simplifying the filters specified for this
---

 Error message                                     Recommended action

 <tablename>)                                      table and its related tables. For best practices, see
                                                   Offline profile guidelines.

 The operation timed out. This may be              Wait and try again later. If possible, solutions
 because of ongoing server updates. Please         should be imported outside of working hours. For
 try again later.                                  more information, see Manage your maintenance
                                                   window.

 An error occurred from ISV code.                  For more information, see Troubleshoot Dataverse
                                                   plug-ins.

 The plug-in execution failed. This is typically   For more information, see Troubleshoot Dataverse
 due to an error in the plug-in code.              plug-ins.

 Internal issue while downloading your data        Look for the error code in Web service error codes.
 (Error code: <errorCode>)

 We are unable to sync offline data for you.       Make sure the user is added to a mobile offline
 No profile assigned to the user.                  profile. For more information, see Set up mobile
                                                   offline (classic).

 We are unable to sync offline data for you.       Make sure the app has a mobile offline profile
 App module has no mobile offline profile          assigned. For more information, see Set up mobile
 assigned.                                         offline (classic).

 We are unable to sync offline data for you.       Make sure that only one profile is selected in the
 Role based profile access is enabled and          model-driven app designer. For more information,
 app module has more than one mobile               see Set up mobile offline (classic).
 offline profile assigned.

 The number of records being downloaded            Modify the filter in the offline profile to download
 exceeds the supported limit. Contact your         fewer records on the device. For best practices, see
 admin to reduce the record count.                 Offline profile guidelines.




Feedback
Was this page helpful?      Yes        No


Provide product feedback
---


## Troubleshooting startup or sign-in issues

Troubleshooting startup or sign-in issues
for Power Apps
ﾃ   Summarize this article for me


This article helps you resolve some common issues or errors that might occur when starting up
or signing in to Power Apps         .



Common issues or errors
The following are some common issues or errors that might appear when you start up or sign
in to Power Apps.

     You're prompted to sign in every time an app is embedded in another client such as
     SharePoint and Microsoft Teams. The Power Apps opening experience starts and halts
     until you sign in.

     Error message related to cookie settings.

       Hmmm... Something went wrong.
       thirdPartyCookiesBlocked
       Please enable third party-cookies and site data in your browser settings. If you are
       using Chrome's Incognito mode, you can uncheck the 'Block third-party cookies'
       option on the Incognito landing page.
       Try again


     "Sign in required" message when signing in to Power Apps, especially in InPrivate or
     incognito mode.

       Sign in required
       Please select sign in to continue.
       Session ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

       AADSTS50058: A silent sign-in request was sent but no user is signed in. The cookies
       used to represent the user's session were not sent in the request to Microsoft Entra
       ID. This can happen if the user is using Internet Explorer or Edge, and the web app
       sending the silent sign-in request is in different IE security zone than the Microsoft
       Entra endpoint (login.microsoftonline.com).
       Trace ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
       Correlation ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
       Timestamp: xxxx-xx-xx xx:xx:xxZ
---

"Hmmm … We couldn't sign you in" message.




"WebAuthoring abnormal termination" message.

  WebAuthoring abnormal termination.

  Client date/time: <Client Time>Thh:mm:ss.sssZ
  Version: 2.0.602
  Session ID: xxxx-xxxxx-xxxxxxx--xxxxxxxx
  description: {"error":{"detail":{"exception":{}},"colno":0,"filename":"
  < https://paaeuscdn.azureedge.net/v2.0.602.0/studio/openSource/modified/winjs/js/
  base.js?v=39de0f2edf1 >...",

  "lineno":0,"message":"Script error","initErrorEvent":"
  [function]","bubbles":false,"cancelBubble":false,"cancelable":false,"currentTarget":"
  [window]", "defaultPrevented":true,
  "eventPhase":2,"isTrusted":true,"srcElement":"[window]","target":"
  [window]","timeStamp":1490711965955,"type":"error","initEvent":"
  [function]","preventDefault":" [function]",
  "stopImmediatePropagation":"[function]","stopPropagation":"
  [function]","AT_TARGET":2,"BUBBLING_PHASE":3,"CAPTURING_PHASE":1},"errorLine":0,
  "errorCharacter":0,
  "errorUrl":"
  < https://paaeuscdn.azureedge.net/v2.0.602.0/studio/openSource/modified/winjs/js/
  base.js?v=39de0f2edf1 >... error","setPromise":"[function]","exception":{}}

  stack: null
---

        errorNumber: 0
        errorMessage: Script error

     UserInterventionNeeded_CookiesBlocked

     UserInterventionNeeded_StorageBlocked

     UserInterventionNeeded_NavigateToAadTimeout

     UserInterventionNeeded_NavigateToAadDenied

     UserInterventionNeeded_StorageLost

     AadError



Resolution
Try the following steps to resolve the issue:

   1. Enable third-party cookies and local data in your browser or app.

   2. Clear your browser's cache and cookies and try again. Cached data can sometimes
     prevent you from signing in.

   3. Try signing in with a different browser. For a list of supported browsers, see system
     requirements.

   4. Check your network connection to make sure it's stable.

   5. If you're getting Microsoft Entra errors, they're usually related to user authentication and
     authorization. The error page might contain additional information that can help
     diagnose and fix the problem. To resolve Microsoft Entra errors, you might need
     assistance from your IT department.

   6. Check the "Third-party Storage Partitioning" setting in your browser to make sure it's
     disabled.


        ７ Note

        Consider this resolution step only when you experience sign-in or sign-out issues
        under one of the following conditions:

             You use a device that has multiple Microsoft Entra identity sign-ins to access
             different applications.
---

              You access multiple applications using Microsoft Entra across more than one
              tab. When you sign out of one tab, you observe that you aren't signed out of
              the second tab.
              You access Power Apps that are embedded via an iframe in a third-party
              website.
              You access a canvas app that's embedded in a model-driven app form.




Check the "Third-party Storage Partitioning" setting in
Microsoft Edge or Google Chrome
       In Microsoft Edge, you can check the setting by navigating to edge://flags/#third-party-
       storage-partitioning using the address bar.

       In Google Chrome, you can check the setting by navigating to chrome://flags/#third-
       party-storage-partitioning using the address bar.




Enable storage of third-party cookies and local
data in your browser or app
Power Apps stores some data locally, such as user identity and preferences, using your
browser's capabilities. Problems occur if the browser blocks the storage of such local data, or
third-party cookies set by Power Apps.

Most browsers allow settings to reflect the changes immediately. You might also need to close
all the browser windows and reopen them instead.

To enable this setting for the Power Apps and Dynamics 365 mobile apps for iOS, you need to
work through the iOS settings linked to the app rather than through the browser settings for
iOS.

These instructions are shown on the following tabs.


  Microsoft Edge
---

       Option 1: Enable storage of third-party cookies and local data for all sites

          1. Select Settings > Cookies and site permissions.
          2. Expand Cookies and data stored.
          3. Ensure the Block third-party cookies setting is disabled.
          4. If present, remove the following sites from the site-specific cookie configuration
             under Block and Clear on exit:
                https://create.powerapps.com

                https://*.create.powerapps.com
                https://make.*.powerapps.com

                https://make.powerapps.com

                https://login.microsoftonline.com
                https://apps.*.powerapps.com

                https://apps.powerapps.com

               (Only for sovereign clouds) US Government version URLs.

       Option 2: Create exceptions to allow the storage of third-party cookies and local data
       for Power Apps and associated services


          ７ Note

          The following steps require your Edge browser version to be 87 or above.


          1. Select Settings > Cookies and site permissions.
          2. Expand Cookies and data stored.
          3. Select Add under Allow and add:
                [*.]powerapps.com

          4. Select Clear browsing data on close.
          5. Ensure Cookies and other site data is disabled. If you want to keep it enabled,
             select Add instead, and then add:
                [*.]powerapps.com




Clear your browser cache
The browser cache is stored on your device's hard drive. When you visit a website, your
browser downloads certain information that allows it to load faster when you revisit the same
website in the future. Some Power Apps features use the browser cache to provide a faster user
---

experience. In some cases, you might want to clear your browser cache. Here are the
instructions for different browsers:

      Microsoft Edge
      Google Chrome
      Safari on Mac



Next steps
If your issue isn't listed in this article, you can search for more support resources   or contact
Microsoft support       . For more information, see Get Help + Support.



 Last updated on 03/12/2026
---
