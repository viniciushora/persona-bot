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

const arcanas = {
    1: "Fool",
    2: "Mago",
    3: "Sacerdotisa",
    4: "Imperatriz",
    5: "Imperador",
    6: "Hierofante",
    7: "Amantes",
    8: "Carruagem",
    9: "Justiça",
    10: "Eremita",
    11: "Fortuna",
    12: "Força",
    13: "Enforcado",
    14: "Morte",
    15: "Sobriedade",
    16: "Diabo",
    17: "Torre",
    18: "Estrela",
    19: "Lua",
    20: "Sol",
    21: "Mundo"
}

const TableCard = props => {

  return (
    <Card elevation={3} className="pt-20 mb-24">
      <div className="card-title px-24 mb-12">Personas</div>
      <div className="overflow-auto">
        <Table className="product-table">
          <TableHead>
            <TableRow>
              <TableCell className="px-24" colSpan={4}>
                Nome
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                ID
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                Arcana
              </TableCell>
              <TableCell className="px-0" colSpan={1}>
                Ação
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.personas.map((persona, index) => (
              <TableRow key={index}>
                <TableCell className="px-0 capitalize" colSpan={4} align="left">
                  <div className="flex flex-middle">
                  <img
                      className="circular-image-small"
                      src={persona.link_foto}
                      alt="user"
                    />
                    <p className="m-0 ml-8">{persona.nome}</p>
                  </div>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{persona.persona_id}</p>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{arcanas[persona.fk_arcana_arcana_id]}</p>
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