package models

type Category struct {
	ID    uint	`json:"id" gorm:"primaryKey"`
	Name  string	`json:"name" validate:"required"`
	Products    []Product `json:"products" gorm:"foreignKey:CategoryID"`
}