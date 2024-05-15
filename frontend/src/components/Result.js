import React from 'react';

function Result({ data }) {
  return (
    <div>
      <h2>Result</h2>
      <p>Name: {data.name}</p>
      <p>Description: {data.description}</p>
      <p>Birthdate: {data.birthdate}</p>
      <p>Gender: {data.gender}</p>
      <p>Partner Birthdate: {data.partnerBirthdate}</p>
      <p>Marriage Date: {data.marriageDate}</p>
      <p>Is Bridegroom: {data.isBridegroom ? 'Yes' : 'No'}</p>
      <p>Add Details: {data.addDetails ? 'Yes' : 'No'}</p>
      <p>Enabled Features: {data.enabledFeatures.join(', ')}</p>
    </div>
  );
}

export default Result;
