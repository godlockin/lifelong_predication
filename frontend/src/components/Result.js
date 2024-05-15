import React from 'react';

function Result({ data }) {
  return (
    <div>
      <p>命主: {data.name}</p>
      <p>生日: {data.birthdate}</p>
      <p>{data.gender ? '男' : '女'}</p>
      {data.partnerBirthdate && <p>配偶生日: {data.partnerBirthdate}</p>} {/* 条件渲染配偶生日 */}
      {data.marriageDate && <p>结婚日期: {data.marriageDate}</p>} {/* 条件渲染结婚日期 */}
      {data.isBridegroom && <p>入赘: {data.isBridegroom ? 'Yes' : 'No'}</p>} {/* 条件渲染是否入赘 */}
      <p>添加更多解释: {data.addDetails ? 'Yes' : 'No'}</p>
      <p>开启功能列表: {data.enabledFeatures.join(', ')}</p>
    </div>
  );
}

export default Result;
