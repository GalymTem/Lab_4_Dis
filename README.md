### Distributed Transactions: 2PC and 3PC
##Laboratory Report (AWS EC2)

## 6. Part 2 — Failure Scenarios (Two-Phase Commit)
# 6.1 Scenario A — Coordinator Crash (Blocking Case)

Goal
To demonstrate the blocking problem inherent in the Two-Phase Commit (2PC) protocol.

Procedure

The coordinator initiates a 2PC transaction.

PREPARE messages are sent to all participants.

All participants respond with VOTE-YES.

The coordinator crashes before sending GLOBAL-COMMIT or GLOBAL-ABORT.

Observed Behavior

Participants remain in the READY state.

Participants cannot commit the transaction.

Participants cannot abort the transaction.

No progress is possible without coordinator recovery.

Screenshots

📸 Screenshot 6.1 — Coordinator process terminated using CTRL+C

📸 Screenshot 6.2 — Participant B /status showing state READY

📸 Screenshot 6.3 — Participant C /status showing state READY

Conclusion

Two-Phase Commit is a blocking protocol. If the coordinator fails after collecting votes but before announcing the final decision, participants remain indefinitely in an uncertain state. This shows that 2PC is not fault-tolerant to coordinator crashes.

# 6.2 Scenario B — Participant Crash

Goal
To observe coordinator behavior when a participant fails before voting.

Procedure

A participant crashes before responding to the PREPARE message.

The coordinator waits until a timeout expires.

The coordinator decides GLOBAL-ABORT.

Observed Behavior

The transaction is aborted.

No participant commits.

Atomicity is preserved.

Screenshot

📸 Screenshot 6.4 — Coordinator output showing transaction aborted due to participant failure

Conclusion

If a participant fails before voting, the coordinator safely aborts the transaction. Atomicity is preserved, although system availability is reduced.

## 7. Part 3 — Three-Phase Commit (3PC)
# 7.1 Protocol Overview

Three-Phase Commit (3PC) improves upon 2PC by introducing an additional phase to avoid blocking.

Phases

CanCommit

PreCommit

DoCommit

Key Idea

Participants never remain in an uncertain state. Assuming bounded communication delays, the system can safely reach a decision even if the coordinator crashes.

# 7.2 Execution and Logs

Command Executed

python3 client.py --coord http://COORD:9100 start TX3 3PC SET z 30


Observed Output

[Coordinator] TX3 CAN-COMMIT
[Participants] VOTE-YES
[Coordinator] PRECOMMIT
[Coordinator] DOCOMMIT


Screenshots

📸 Screenshot 7.1 — Client output showing transaction TX3 committed

📸 Screenshot 7.2 — Participant /status showing state COMMITTED

Conclusion

Unlike 2PC, the Three-Phase Commit protocol does not block. Participants can safely progress and complete the transaction even if the coordinator fails after the PreCommit phase.

## 8. Comparison — Two-Phase Commit vs Three-Phase Commit
Feature	2PC	3PC
Atomicity	Yes	Yes
Blocking possible	Yes	No
Coordinator crash tolerance	No	Yes
Protocol complexity	Low	Higher
Additional phase	No	Yes
##9. Safety and Correctness Analysis
#9.1 Atomicity

Transactions either commit on all participants or abort everywhere.

# 9.2 Consistency

All nodes reach the same final decision for each transaction.

# 9.3 Fault Tolerance

2PC blocks if the coordinator crashes.

3PC avoids blocking under bounded network delays.

## 10. Final Conclusion

This laboratory successfully implemented and evaluated distributed transaction protocols on AWS EC2.

Key Results

Correct atomic execution of distributed transactions

Clear demonstration of the blocking limitation in 2PC

Successful non-blocking execution using 3PC

Practical understanding of coordination, failures, and recovery mechanisms

The experiments confirm the theoretical properties of Two-Phase Commit and Three-Phase Commit and clearly demonstrate why 3PC provides improved fault tolerance in real distributed environments.

