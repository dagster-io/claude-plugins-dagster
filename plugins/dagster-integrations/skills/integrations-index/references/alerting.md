# Alerting Integrations

Notification and alerting systems for pipeline monitoring, team communication, and incident
management.

---

### Slack

**Package:** `dagster-slack` | **Support:** Dagster-supported

Send notifications and alerts to Slack channels for pipeline monitoring and team communication.

**Use cases:**

- Alert team on pipeline failures
- Send success notifications
- Share data quality reports
- Post daily pipeline summaries

**Quick start:**

```python
from dagster_slack import SlackResource

slack = SlackResource(
    token=dg.EnvVar("SLACK_BOT_TOKEN")
)

@dg.asset
def notify_completion(
    context: dg.AssetExecutionContext,
    slack: SlackResource
):
    slack.get_client().chat_postMessage(
        channel="#data-alerts",
        text=f"Asset {context.asset_key} completed successfully!"
    )
```

**Using sensors:**

```python
from dagster_slack import make_slack_on_run_failure_sensor

slack_failure_sensor = make_slack_on_run_failure_sensor(
    channel="#alerts",
    slack_token=dg.EnvVar("SLACK_BOT_TOKEN")
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/slack

---

### PagerDuty

**Package:** `dagster-pagerduty` | **Support:** Dagster-supported

Create incidents and send alerts to PagerDuty for on-call incident management.

**Use cases:**

- Create incidents for critical pipeline failures
- Escalate data quality issues
- On-call alerting for production issues
- Integrate with incident response workflows

**Quick start:**

```python
from dagster_pagerduty import PagerDutyResource

pagerduty = PagerDutyResource(
    routing_key=dg.EnvVar("PAGERDUTY_ROUTING_KEY")
)

@dg.asset
def critical_alert(pagerduty: PagerDutyResource):
    pagerduty.trigger_incident(
        severity="critical",
        summary="Data pipeline failure in production",
        source="dagster-pipeline",
        custom_details={
            "pipeline": "daily_etl",
            "error": "Connection timeout"
        }
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/pagerduty

---

### Microsoft Teams

**Package:** `dagster-msteams` | **Support:** Dagster-supported

Send notifications to Microsoft Teams channels for pipeline monitoring.

**Use cases:**

- Alert teams using Microsoft Teams
- Send pipeline status updates
- Share data reports in Teams channels
- Enterprise communication integration

**Quick start:**

```python
from dagster_msteams import MSTeamsResource

teams = MSTeamsResource(
    hook_url=dg.EnvVar("MSTEAMS_WEBHOOK_URL")
)

@dg.asset
def teams_notification(teams: MSTeamsResource):
    teams.get_client().post_message(
        title="Pipeline Complete",
        message="Daily ETL pipeline finished successfully",
        theme_color="00FF00"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/msteams

---

### Twilio

**Package:** `dagster-twilio` | **Support:** Dagster-supported

Send SMS messages and make phone calls for critical alerts.

**Use cases:**

- SMS alerts for critical failures
- Phone call escalation for urgent issues
- Send verification codes
- Multi-channel alerting

**Quick start:**

```python
from dagster_twilio import TwilioResource

twilio = TwilioResource(
    account_sid=dg.EnvVar("TWILIO_ACCOUNT_SID"),
    auth_token=dg.EnvVar("TWILIO_AUTH_TOKEN")
)

@dg.asset
def critical_sms_alert(twilio: TwilioResource):
    twilio.get_client().messages.create(
        from_="+1234567890",
        to="+0987654321",
        body="CRITICAL: Production pipeline failed"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/twilio

---

### Apprise

**Package:** `dagster-apprise` | **Support:** Community-supported

Universal notification library supporting 80+ services (Discord, Telegram, Email, etc.).

**Use cases:**

- Send notifications to multiple services
- Use services without dedicated integrations
- Centralized notification configuration
- Multi-channel alerting

**Quick start:**

```python
from dagster_apprise import AppriseResource

apprise = AppriseResource(
    urls=[
        "discord://webhook_id/webhook_token",
        "mailto://user:pass@gmail.com"
    ]
)

@dg.asset
def multi_channel_alert(apprise: AppriseResource):
    apprise.notify(
        title="Pipeline Alert",
        body="Daily pipeline completed successfully"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/apprise

---

### DingTalk

**Package:** `dagster-dingtalk` | **Support:** Community-supported

Send notifications to DingTalk (popular in China) for team communication.

**Use cases:**

- Notify teams using DingTalk
- Send pipeline alerts in Chinese organizations
- Integration with Asian enterprise tools

**Quick start:**

```python
from dagster_dingtalk import DingTalkResource

dingtalk = DingTalkResource(
    webhook_url=dg.EnvVar("DINGTALK_WEBHOOK"),
    secret=dg.EnvVar("DINGTALK_SECRET")
)

@dg.asset
def dingtalk_notification(dingtalk: DingTalkResource):
    dingtalk.send_message(
        "Pipeline completed successfully"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/dingtalk

---

## Alerting Tool Selection

| Tool          | Best For             | Type          | Urgency    |
| ------------- | -------------------- | ------------- | ---------- |
| **Slack**     | Team communication   | Chat          | Low-Medium |
| **MS Teams**  | Enterprise Microsoft | Chat          | Low-Medium |
| **PagerDuty** | On-call incidents    | Incident Mgmt | High       |
| **Twilio**    | SMS/Voice alerts     | Communication | Critical   |
| **Apprise**   | Multi-platform       | Universal     | All levels |
| **DingTalk**  | Asian markets        | Chat          | Low-Medium |

## Common Patterns

### Run Failure Sensor

```python
from dagster_slack import make_slack_on_run_failure_sensor

@dg.run_failure_sensor
def slack_on_failure(context: dg.RunFailureContext, slack: SlackResource):
    slack.get_client().chat_postMessage(
        channel="#alerts",
        text=f"❌ Run {context.run_id} failed!\n"
             f"Error: {context.failure_event.message}"
    )
```

### Multi-Channel Alerting

```python
@dg.asset
def critical_pipeline(
    slack: SlackResource,
    pagerduty: PagerDutyResource,
    twilio: TwilioResource
):
    try:
        result = process_critical_data()
        slack.post_message("#alerts", "✅ Success")
        return result
    except Exception as e:
        # Alert multiple channels
        slack.post_message("#alerts", f"❌ Failure: {e}")
        pagerduty.trigger_incident(
            severity="critical",
            summary=str(e)
        )
        twilio.send_sms(
            to="+1234567890",
            body=f"CRITICAL: {e}"
        )
        raise
```

### Escalation Pattern

```python
@dg.asset
def monitored_pipeline(
    slack: SlackResource,
    pagerduty: PagerDutyResource
):
    try:
        result = process_data()
        return result
    except MinorError as e:
        # Log to Slack, don't page
        slack.post_message("#warnings", f"⚠️ Warning: {e}")
        return handle_minor_error()
    except CriticalError as e:
        # Alert via Slack AND page on-call
        slack.post_message("#alerts", f"🚨 CRITICAL: {e}")
        pagerduty.trigger_incident(
            severity="critical",
            summary=str(e)
        )
        raise
```

## Tips

- **Alert fatigue**: Don't alert on every event - focus on actionable alerts
- **Severity levels**: Use appropriate channels for different severity levels
- **Context**: Include relevant context (run ID, asset, error message) in alerts
- **Testing**: Test alerting integrations before production deployment
- **Sensors**: Use sensors for automatic alerting on run/asset failures
- **Escalation**: Use PagerDuty/Twilio for critical issues requiring immediate action
- **Batching**: Consider batching non-critical notifications to reduce noise
- **Rate limiting**: Implement rate limits to prevent alert storms
- **On-call rotation**: Integrate with PagerDuty for managed on-call rotations
