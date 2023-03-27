# History

Algorand was founded in 2017 by Silvio Micali, a professor at MIT. The Algorand test network was launched to the public in April 2019, and the main network was launched in June 2019. Algorand has a negligible energy consumption per transaction.

# Governance

Algorand is composed of a company and a foundation. The Algorand Foundation manages award funding, cryptographic research, on-chain governance, and decentralization of the Algorand network including nodes. The core development of the Algorand protocol is overseen by Algorand Inc., a private corporation based in Boston. The Algorand Foundation was led by cryptographer Tal Rabin.

The Algorand Foundation issues quarterly votes for the stakers of ALGO to vote on. These proposals often revolve around the implementation of DeFi within the Algorand community.

# Design

Algorand is intended to solve the "blockchain trilemma": the claim that any blockchain system can have at most two of three desirable properties: decentralization, scalability, and security. A system with all three could run on nodes which each have only moderate consumer-grade resources, has transaction processing which scales with the total network resources, and could not be subverted by attackers who individually possess a large fraction of the network's total resources.

# Consensus algorithm

Algorand uses a Byzantine agreement protocol that leverages proof of stake. As long as a supermajority of the stake is in non-malicious hands, the protocol can tolerate malicious users, achieving consensus without a central authority.

Consensus on Algorand requires three steps to propose, confirm and write the block to the blockchain. The steps are propose, soft vote, and certify vote.

The first phase (the block proposal phase) uses proof of stake principles. During this phase, a committee of users in the system is selected randomly, though in a manner that is weighted, to propose the new block. The selection of the committee is done via a process called "cryptographic sortition", where each user determines whether they are on the committee by locally executing a Verifiable random function (VRF). If the VRF indicates that the user is chosen, the VRF returns a cryptographic proof that can be used to verify that the user is on the committee. The likelihood that a given user will be on the committee is influenced by the number of ALGO tokens held by that user (the stake).

After determining a user is on the block selection committee, that user can build a proposed block and disseminates it to the network for review/analysis during the second phase. The user includes the cryptographic proof from the VRF in their proposed block to demonstrate committee membership.

In the second phase (the block finalization phase), a Byzantine Agreement protocol (called "BA\*") is used to vote on the proposed blocks. In this second phase, a new committee is formed via cryptographic sortition. When users have determined that they are in this second-phase voting committee, they analyze the proposed blocks they have received (including verification of first-phase committee membership) and vote on whether any of the blocks should be adopted. If the voting committee achieves consensus on a new block, then the new block is disseminated across the network.

Within the Algorand consensus algorithm, membership in both committees changes every time the phase is run. This protects users against targeted attacks, as an attacker will not know in advance which users are going to be in a committee. Two different Algorand blocks cannot reach consensus in the same round. According to an external security audit, the model also accounts for timing issues and adversary actions, e.g., when the adversary has control over message delivery.
