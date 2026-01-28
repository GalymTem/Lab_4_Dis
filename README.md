# Distributed Transactions: 2PC and 3PC
## Laboratory Report (AWS EC2)

## 6. Part 2 — Failure Scenarios (Two-Phase Commit)
### 6.1 Scenario A — Coordinator Crash (Blocking Case)

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

<img width="569" height="53" alt="image" src="https://github.com/user-attachments/assets/7152f54f-08a7-467c-a273-32b1c253d6eb" />

<img width="570" height="57" alt="image" src="https://github.com/user-attachments/assets/b93b99c4-66f6-4c7b-9e03-829999ce0773" />

Conclusion

Two-Phase Commit is a blocking protocol. If the coordinator fails after collecting votes but before announcing the final decision, participants remain indefinitely in an uncertain state. This shows that 2PC is not fault-tolerant to coordinator crashes.

### 6.2 Scenario B — Participant Crash

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

If a participant fails before voting, the coordinator safely aborts the transaction. Atomicity is preserved, although system availability is reduced.

## 7. Part 3 — Three-Phase Commit (3PC)
### 7.1 Protocol Overview

Three-Phase Commit (3PC) improves upon 2PC by introducing an additional phase to avoid blocking.

Phases

CanCommit

PreCommit

DoCommit

Key Idea

Participants never remain in an uncertain state. Assuming bounded communication delays, the system can safely reach a decision even if the coordinator crashes.

### 7.2 Execution and Logs

Command Executed

python3 client.py --coord http://COORD:9100 start TX3 3PC SET z 30


Observed Output

[Coordinator] TX3 CAN-COMMIT
[Participants] VOTE-YES
[Coordinator] PRECOMMIT
[Coordinator] DOCOMMIT


Screenshots

<img width="717" height="103" alt="image" src="https://github.com/user-attachments/assets/08d5d205-392b-4e24-a015-2b6b1e52af7c" />

<img width="1024" height="91" alt="image" src="https://github.com/user-attachments/assets/166a325a-10ce-4fc0-a3b7-fec93ebe09dd" />


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
###9.1 Atomicity

Transactions either commit on all participants or abort everywhere.

### 9.2 Consistency

All nodes reach the same final decision for each transaction.

### 9.3 Fault Tolerance

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

