import React, { useState } from "react";

function Payments() {
  const [paymentData, setPaymentData] = useState({
    creditCardNumber: "",
    expirationDate: "",
    cvc: "",
    amount: ""
  });

  const handleChange = (e) => {
    setPaymentData({
      ...paymentData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://localhost:8080/payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        creditCardNumber: paymentData.creditCardNumber,
        expirationDate: paymentData.expirationDate,
        cvc: parseInt(paymentData.cvc),
        amount: parseInt(paymentData.amount)
      })
    })
      .then((response) => {
        if (response.ok) {
          alert("Płatność wysłana!");
        } else {
          alert("Błąd przy wysyłaniu płatności.");
        }
      })
      .catch((error) => console.error("Błąd podczas wysyłania zapytania:", error));
  };

  return (
    <div className="form-wrapper">
      <h2>Płatności</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="creditCardNumber"
          placeholder="Numer karty"
          value={paymentData.creditCardNumber}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="expirationDate"
          placeholder="Data ważności (MM/YY)"
          value={paymentData.expirationDate}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="cvc"
          placeholder="CVC"
          value={paymentData.cvc}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="amount"
          placeholder="Kwota do zapłaty"
          value={paymentData.amount}
          onChange={handleChange}
          required
        />
        <button type="submit">Zapłać</button>
      </form>
    </div>
  );
}

export default Payments;
