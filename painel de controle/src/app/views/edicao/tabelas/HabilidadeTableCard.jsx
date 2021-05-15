import React, { Component } from "react";
import {
  Card,
  Icon,
  IconButton,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody
} from "@material-ui/core";

const elementos = {
    1: "Físico",
    2: "Arma de Fogo",
    3: "Fogo",
    4: "Gelo",
    5: "Elétrico",
    6: "Vento",
    7: "Psy",
    8: "Nuclear",
    9: "Benção",
    10: "Maldição",
    11: "Onipotência",
    12: "Doença",
    13: "Cura",
    14: "Suporte",
    15: "Passiva",
    16: "Navegação"
}

const TableCard = props => {

  return (
    <Card elevation={3} className="pt-20 mb-24">
      <div className="card-title px-24 mb-12">Habilidades</div>
      <div className="overflow-auto">
        <Table className="product-table">
          <TableHead>
            <TableRow>
              <TableCell className="px-24" colSpan={4}>
                Nome
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                Elemento
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                ID
              </TableCell>
              <TableCell className="px-0" colSpan={1}>
                Ação
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.habilidades.map((habilidade, index) => (
              <TableRow key={index}>
                <TableCell className="px-0 capitalize" colSpan={4} align="left">
                  <div className="flex flex-middle">
                    <p className="m-0 ml-8">{habilidade.nome}</p>
                  </div>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{elementos[habilidade.habilidade_id]}</p>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{habilidade.habilidade_id}</p>
                </TableCell>
                <TableCell className="px-0" colSpan={1}>
                  <IconButton>
                    <Icon color="primary">edit</Icon>
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </Card>
  );
};

export default TableCard;
