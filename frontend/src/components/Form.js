import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import 'react-datepicker/dist/react-datepicker.css';

function Form({ onResult }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [birthdate, setBirthdate] = useState(new Date());
  const [gender, setGender] = useState('');
  const [partnerBirthdate, setPartnerBirthdate] = useState(null);
  const [marriageDate, setMarriageDate] =useState(null);
  const [isBridegroom, setIsBridegroom] = useState(false);
  const [addDetails, setAddDetails] = useState(false);
  const [enabledFeatures, setEnabledFeatures] = useState([]);
  const [featuresOptions, setFeaturesOptions] = useState([]);

  useEffect(() => {
    // 从后端获取功能选项
    const fetchFeatures = async () => {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/prediction/features`);
      const data = await response.json();
      const options = Object.keys(data).map(key => ({
        value: key,
        label: data[key]
      }));
      setFeaturesOptions(options);
    };
    fetchFeatures();
  }, []);

  const genderOptions = [
    { value: 'male', label: '男' },
    { value: 'female', label: '女' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/prediction/process/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        description,
        birthdate,
        gender,
        partnerBirthdate,
        marriageDate,
        isBridegroom,
        addDetails,
        enabledFeatures,
      }),
    });
    const data = await response.json();
    onResult(data);
  };

  return (
      <form onSubmit={handleSubmit}>
        <div>
          <label>命主姓名:</label>
          <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              required
          />
        </div>
        <div>
          <label>命主生日:</label>
          <DatePicker
              selected={birthdate}
              onChange={date => setBirthdate(date)}
              showTimeSelect
              dateFormat="Pp"
              required
          />
        </div>
        <div>
          <label>命主性别:</label>
          <Select
              options={genderOptions}
              value={genderOptions.find(option => option.value === gender)}
              onChange={option => setGender(option.value)}
          />
        </div>
        <div>
          <label>命主对象生日:</label>
          <DatePicker
              selected={partnerBirthdate}
              onChange={date => setPartnerBirthdate(date)}
              showTimeSelect
              dateFormat="Pp"
              isClearable
          />
        </div>
        <div>
          <label>命主结婚日期:</label>
          <DatePicker
              selected={marriageDate}
              onChange={date => setMarriageDate(date)}
              showTimeSelect
              dateFormat="Pp"
              isClearable
          />
        </div>
        <div>
          <label>
            <input
                type="checkbox"
                checked={isBridegroom}
                onChange={() => setIsBridegroom(!isBridegroom)}
            />
            命主婚姻是否存在入赘
          </label>
        </div>
        <div>
          <label>
            <input
                type="checkbox"
                checked={addDetails}
                onChange={() => setAddDetails(!addDetails)}
            />
            添加详情
          </label>
        </div>
        <div>
          <label>开启功能:</label>
          <Select
              options={featuresOptions}
              isMulti
              value={featuresOptions.filter(option => enabledFeatures.includes(option.value))}
              onChange={options => setEnabledFeatures(options.map(option => option.value))}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
  );
}

export default Form;
