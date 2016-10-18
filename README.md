smtpd_helo_restrictions =
  check_policy_service inet:127.0.0.1:10023
smtpd_recipient_restrictions =
  check_policy_service inet:127.0.0.1:10024

