// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Certification {
    struct Certificate {
        string candidate_name;
        string grad_number;
        string place_of_birth;
        // uint diploma_mark_num;      //might interfere (not string)
        string diploma_mark;
        string ipfs_hash;
    }

    mapping(string => Certificate) public certificates;
    event certificateGenerated(string certificate_id);

    function generateCertificate(
        string memory _certificate_id,
        string memory _candidate_name,
        string memory _grad_number,
        string memory _place_of_birth,
        string memory _diploma_mark,
        string memory _ipfs_hash
    ) public {
        // Check if certificate with the given ID already exists
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length == 0,
            "Certificate with this ID already exists"
        );

        // Create the certificate
        Certificate memory cert = Certificate({
            candidate_name: _candidate_name,
            grad_number: _grad_number,
            place_of_birth: _place_of_birth,
            diploma_mark: _diploma_mark,
            ipfs_hash: _ipfs_hash
        });

        // Store the certificate in the mapping
        certificates[_certificate_id] = cert;

        // Emit an event
        emit certificateGenerated(_certificate_id);
    }

    function getCertificate(
        string memory _certificate_id
    )
        public
        view
        returns (
            string memory _candidate_name,
            string memory _grad_number,
            string memory _place_of_birth,
            string memory _diploma_mark,
            string memory _ipfs_hash
        )
    {
        Certificate memory cert = certificates[_certificate_id];

        // Check if the certificate with the given ID exists
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length != 0,
            "Certificate with this ID does not exist"
        );

        // Return the values from the certificate
        return (
            cert.candidate_name,
            cert.grad_number,
            cert.place_of_birth,
            cert.diploma_mark,
            cert.ipfs_hash
        );
    }

    function isVerified(
        string memory _certificate_id) public view returns (bool) {
        return bytes(certificates[_certificate_id].ipfs_hash).length != 0;
    }
}
